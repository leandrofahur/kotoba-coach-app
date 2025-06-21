import { Badge } from "@/components/ui/badge";
import { LessonStatus } from "@/components/LessonBlock/LessonBlock.types";

import {Check, Volume1} from 'lucide-react'


function LessonBadge({ lessonStatus }: { lessonStatus: LessonStatus }) {

    const mapLessonStatusToBadge = (status: LessonStatus) => {
        switch (status) {
            case LessonStatus.COMPLETED:
                return "bg-primary";
            case LessonStatus.IN_PROGRESS:
                return "bg-secondary";
            default:
                return "";
        }
    }

    const mapLessonStatusToIcon = (status: LessonStatus) => {
        switch (status) {
            case LessonStatus.COMPLETED:
                return <Check className="size-4"/>;
            case LessonStatus.IN_PROGRESS:
                return <Volume1 className="size-4"/>;
        }
    }

    return (
        <Badge className={`text-center capitalize text-[12px] font-[600] leading-[22px] ${mapLessonStatusToBadge(lessonStatus)}`}>
            <span>
                {mapLessonStatusToIcon(lessonStatus)}
            </span>
            
                {lessonStatus.replace('-', ' ')}
            
        </Badge>
    )
}

export default LessonBadge;