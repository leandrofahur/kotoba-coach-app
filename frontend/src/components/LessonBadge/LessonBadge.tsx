import { Badge } from "@/components/ui/badge";
import { LessonStatus } from "@/components/LessonBlock/LessonBlock.types";

import {Check, Mic} from 'lucide-react'


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
                return <Check className="w-4 h-4"/>;
            case LessonStatus.IN_PROGRESS:
                return <Mic className="w-4 h-4"/>;
        }
    }

    return (
        <Badge className={`text-center capitalize text-[12px] fond-[600] leading-[22px]  ${mapLessonStatusToBadge(lessonStatus)}`}>
            {mapLessonStatusToIcon(lessonStatus)} {lessonStatus.replace('-', ' ')}
        </Badge>
    )
}

export default LessonBadge;