"""Collection permission routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...auth.dependencies import get_current_user
from ...database import get_db
from ...models.collection import Collection
from ...models.user import User
from .schemas import (
    BulkPermissionGrantRequest,
    PermissionLogWithUserResponse,
    PermissionResponse,
    UserPermissionResponse,
)
from .service import CollectionPermissionService

router = APIRouter(tags=["collection-permissions"])


def get_permission_service(
    db: Session = Depends(get_db),
) -> CollectionPermissionService:
    """Get permission service dependency."""
    return CollectionPermissionService(db)


def get_collection_with_modify_permission_local(
    collection_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Collection:
    """Get collection with modify permission or raise error (local version to avoid circular imports)."""
    from ..service import CollectionService

    collection_service = CollectionService(db)
    collection = collection_service.get_collection(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )

    # Check modify permission
    if not collection_service._can_modify_collection(collection, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this collection",
        )

    return collection


@router.post(
    "/{collection_id}/permissions",
    response_model=list[PermissionResponse],
    status_code=status.HTTP_201_CREATED,
)
def grant_permission(
    collection_id: str,
    permission_data: BulkPermissionGrantRequest,
    current_user: User = Depends(get_current_user),
    permission_service: CollectionPermissionService = Depends(get_permission_service),
    collection: Collection = Depends(get_collection_with_modify_permission_local),
):
    """Grant permissions to multiple users for a collection."""
    # Only collection OWNER can grant permissions
    if not permission_service.can_owner_collection(collection_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only collection OWNER can grant permissions",
        )

    granted_permissions = []
    for permission_request in permission_data.permissions:
        permission = permission_service.grant_permission(
            collection_id=collection_id,
            user_id=permission_request.user_id,
            permission_level=permission_request.permission_level,
            granted_by=current_user,
        )
        granted_permissions.append(PermissionResponse.model_validate(permission))

    return granted_permissions


@router.delete(
    "/{collection_id}/permissions/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def revoke_permission(
    collection_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user),
    permission_service: CollectionPermissionService = Depends(get_permission_service),
    collection: Collection = Depends(get_collection_with_modify_permission_local),
):
    """Revoke permission from a user for a collection."""
    # Only collection OWNER can revoke permissions
    if not permission_service.can_owner_collection(collection_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only collection OWNER can revoke permissions",
        )

    permission_service.revoke_permission(
        collection_id=collection_id,
        user_id=user_id,
        revoked_by=current_user,
    )


@router.get(
    "/{collection_id}/permissions",
    response_model=list[UserPermissionResponse],
)
def list_collection_permissions(
    collection_id: str,
    current_user: User = Depends(get_current_user),
    permission_service: CollectionPermissionService = Depends(get_permission_service),
    collection: Collection = Depends(get_collection_with_modify_permission_local),
):
    """List all permissions for a collection."""
    if not permission_service.can_owner_collection(collection_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only collection OWNER can view permissions",
        )

    permissions = permission_service.get_user_permissions(collection_id)

    # Convert to response with user details
    response_permissions = []
    for permission in permissions:
        user = permission.user
        granter = permission.granter
        response_permissions.append(
            UserPermissionResponse(
                id=permission.id,
                collection_id=permission.collection_id,
                user_id=permission.user_id,
                username=user.username,
                email=user.email,
                permission_level=permission.permission_level,
                granted_by=permission.granted_by,
                granter_username=granter.username,
                created_at=permission.created_at,
                updated_at=permission.updated_at,
            )
        )

    return response_permissions


@router.get(
    "/{collection_id}/permissions/me",
    response_model=PermissionResponse,
)
def get_my_permission(
    collection_id: str,
    current_user: User = Depends(get_current_user),
    permission_service: CollectionPermissionService = Depends(get_permission_service),
    collection: Collection = Depends(get_collection_with_modify_permission_local),
):
    """Get current user's permission for a collection."""
    permission = permission_service.get_user_permission(collection_id, current_user.id)

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No permission found for this user",
        )

    return PermissionResponse.model_validate(permission)


@router.get(
    "/{collection_id}/permissions/logs",
    response_model=list[PermissionLogWithUserResponse],
)
def get_permission_logs(
    collection_id: str,
    current_user: User = Depends(get_current_user),
    permission_service: CollectionPermissionService = Depends(get_permission_service),
    collection: Collection = Depends(get_collection_with_modify_permission_local),
):
    """Get permission audit logs for a collection."""
    # Only collection OWNER can view permission logs
    if not permission_service.can_owner_collection(collection_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only collection OWNER can view permission logs",
        )

    logs = permission_service.get_permission_logs(collection_id)

    # Convert to response with user details
    response_logs = [
        PermissionLogWithUserResponse(
            id=log.id,
            collection_id=log.collection_id,
            user_id=log.user_id,
            username=log.user.username,
            email=log.user.email,
            action=log.action,
            permission_level=log.permission_level,
            performed_by=log.performed_by,
            performer_username=log.performer.username,
            created_at=log.created_at,
        )
        for log in logs
    ]

    return response_logs
