import { useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { LessonStatus, type LessonBlockProps } from "./LessonBlock.types";
import LessonBadge from "@/components/LessonBadge/LessonBadge";

export default function LessonBlock({ id, text, romaji, translation, audio_url, status = LessonStatus.NOT_STARTED }: LessonBlockProps) {
    const navigate = useNavigate();

    const handleClick = () => {
        if(status !== LessonStatus.NOT_STARTED) {
            navigate(`/lessons/${id}`, { 
                state: { lesson: { id, text, romaji, translation, audio_url, status } }
            });
        }
    };

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
    <Card 
      className={`w-full max-w-md shadow-[#C7C7C7] ${mapLessonStatusToColor(status)} cursor-pointer hover:opacity-80 transition-opacity`} 
      onClick={handleClick}
    >
      <CardContent>
        <div className="flex justify-between">
            <p className={`text-center ${mapLessonStatusToTextColor(status)}`}>Lesson {id}</p>
            {status !== LessonStatus.NOT_STARTED && <LessonBadge lessonStatus={status} />}
        </div>        
      </CardContent>
    </Card>
  );
}