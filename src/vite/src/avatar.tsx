import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

export function AvatarIcon ({ avatarUrl }: { avatarUrl: string }) {
  return (
    <div className="flex flex-row flex-wrap items-center gap-12">
      <Avatar>
        <AvatarImage src={avatarUrl} alt="@avatar" />
        <AvatarFallback>CN</AvatarFallback>
      </Avatar>
    </div>
  )
}
