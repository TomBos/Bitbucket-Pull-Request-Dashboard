import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

type Person = {
  display_name: string
  avatar: string
}

type Entry = {
  id: number
  title: string
  author: string,
  summary: {
    html: string
  }
  reviewers: Person[]
  participants: Person[]
}

type AccordionElementProps = {
  entries: Entry[]
}

function renderAvatar(person: Person) {
  const initials = person.display_name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .toUpperCase()

  return (
    <div className="flex items-center gap-2" key={person.display_name}>
      <Avatar>
        <AvatarImage src={person.avatar} alt={person.display_name} />
        <AvatarFallback>{initials}</AvatarFallback>
      </Avatar>
      <span className="text-sm">{person.display_name}</span>
    </div>
  )
}

export function AccordionElement({ entries }: AccordionElementProps) {
  return (
    <Accordion type="single" collapsible className="w-full" defaultValue={`item-${entries[0]?.id}`}>
      {entries.map((entry) => (
        <AccordionItem key={entry.id} value={`item-${entry.id}`}>
          <AccordionTrigger>{entry.title}</AccordionTrigger>
          <AccordionContent className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <p className="font-semibold text-muted-foreground text-xs uppercase">Author</p>
              {entry.author}
            </div>
            <div
              className="prose max-w-none"
              dangerouslySetInnerHTML={{ __html: entry.summary.html || ""}}
            />
            <div className="flex flex-col gap-2">
              {entry.reviewers?.length > 0 && (
                <>
                  <p className="font-semibold text-muted-foreground text-xs uppercase">Reviewers</p>
                  {entry.reviewers.map(renderAvatar)}
                </>
              )}
              {entry.participants?.length > 0 && (
                <>
                  <p className="font-semibold text-muted-foreground text-xs uppercase mt-4">Participants</p>
                  {entry.participants.map(renderAvatar)}
                </>
              )}
            </div>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  )
}
