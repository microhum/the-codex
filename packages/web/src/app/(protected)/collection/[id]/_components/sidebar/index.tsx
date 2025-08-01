"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { FilePlus2Icon, UserIcon } from "lucide-react";

import ClusteringTree from "@/app/(protected)/collection/[id]/_components/clustering/tree";
import CollectionIdSidebarSearchbox from "@/app/(protected)/collection/[id]/_components/sidebar/search";
import CollectionIdSidebarSettings from "@/app/(protected)/collection/[id]/_components/sidebar/settings";
import { useCollectionIdContext } from "@/app/(protected)/collection/[id]/_components/use-collection-id-context";
import { Logo } from "@/components/icon";
import SettingDialog from "@/components/settings/dialog";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Sidebar,
  SidebarGroup,
  SidebarHeader,
  SidebarSeparator,
} from "@/components/ui/sidebar";

function CollectionIdSidebar() {
  const context = useCollectionIdContext();

  const params = useParams<{ id: string }>();

  return (
    <Sidebar>
      <SidebarHeader className="flex flex-row items-center justify-between p-4">
        <Link href="/home">
          <Logo size={80} />
        </Link>
        <SettingDialog
          icon={
            <Button size="icon" className="rounded-full" variant="ghost">
              <Avatar>
                <AvatarImage src="" />
                <AvatarFallback>
                  <UserIcon className="size-4" />
                </AvatarFallback>
              </Avatar>
            </Button>
          }
        />
      </SidebarHeader>
      <SidebarSeparator />
      <div className="flex min-h-0 flex-1 flex-col gap-6 overflow-auto p-4 group-data-[collapsible=icon]:overflow-hidden">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold">{context.title}</h1>
          <CollectionIdSidebarSettings />
        </div>
        <p className="text-muted-foreground text-sm font-light">
          {context.description}
        </p>
        <Separator />
        <div className="flex w-full gap-2">
          <CollectionIdSidebarSearchbox />
          <Link href={`/collection/${params.id}/docs`}>
            <Button size="icon" variant="outline">
              <FilePlus2Icon />
            </Button>
          </Link>
        </div>
        <SidebarGroup className="p-0">
          <ClusteringTree />
        </SidebarGroup>
      </div>
    </Sidebar>
  );
}

export default CollectionIdSidebar;
