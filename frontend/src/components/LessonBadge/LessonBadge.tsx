import { Badge } from "@/components/ui/badge";
import { LessonStatus } from "@/components/LessonBlock/LessonBlock.types";

// import IconCheckWhite from "@/assets/icons/check.svg";
// import IconProgressWhite from "@/assets/icons/progress.svg";

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
                return <Check width={20} height={20}/>;
            case LessonStatus.IN_PROGRESS:
                return <Mic width={20} height={20}/>;
        }
    }

    return (
        <Badge className={`text-center capitalize ${mapLessonStatusToBadge(lessonStatus)}`}>
            {mapLessonStatusToIcon(lessonStatus)} {lessonStatus.replace('-', ' ')}
        </Badge>
    )
}

export default LessonBadge;