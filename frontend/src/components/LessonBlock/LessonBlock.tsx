import { Card, CardContent } from "@/components/ui/card";
import { type LessonBlockProps, LessonStatus } from "@/components/LessonBlock/LessonBlock.types";

import LessonBadge from "@/components/LessonBadge/LessonBadge";

export default function LessonBlock({ lessonNumber, lessonStatus = LessonStatus.NOT_STARTED }: LessonBlockProps) {

    const mapLessonStatusToColor = (status: LessonStatus) => {
        switch (status) {
            case LessonStatus.COMPLETED:
                return "bg-primary-dark";
            case LessonStatus.IN_PROGRESS:
                return "bg-primary";
            case LessonStatus.NOT_STARTED:
                return "bg-gray-light";
        }
    }

    const mapLessonStatusToTextColor = (status: LessonStatus) => {
        switch (status) {        
            case LessonStatus.NOT_STARTED:
                return "text-gray";
            default:
                return "text-white";
        }
    }

  return (
    <Card className={`w-full max-w-md shadow-[#C7C7C7] ${mapLessonStatusToColor(lessonStatus)}`} >
      <CardContent>
        <div className="flex justify-between">
            <p className={`text-center ${mapLessonStatusToTextColor(lessonStatus)}`}>Lesson {lessonNumber}</p>
            {lessonStatus !== LessonStatus.NOT_STARTED && <LessonBadge lessonStatus={lessonStatus} />}
        </div>
      </CardContent>
    </Card>
  );
}