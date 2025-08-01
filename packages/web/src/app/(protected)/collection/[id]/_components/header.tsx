"use client";

import { useCollectionIdContext } from "@/app/(protected)/collection/[id]/_components/use-collection-id-context";
import { ToggleThemeButton } from "@/components/button/toggle-theme";
import { SidebarTrigger, useSidebar } from "@/components/ui/sidebar";

function CollectionIdHeader() {
  const context = useCollectionIdContext();
  const { state } = useSidebar();

  return (
    <div className="mb-2 flex w-full items-center justify-between gap-4">
      <div className="flex items-center gap-2">
        <SidebarTrigger />
        {state == "collapsed" && <span>{context.title}</span>}
      </div>

      <ToggleThemeButton />
    </div>
  );
}
export default CollectionIdHeader;
