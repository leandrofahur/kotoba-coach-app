import LessonBlock from "@/components/LessonBlock/LessonBlock";
import type { LessonBlockListProps } from "./LessonBlockList.types";

function LessonBlockList({ lessonBlocks }: LessonBlockListProps) {    
    return (
        <div className="flex flex-col items-center justify-center h-screen bg-beige-light p-4 gap-4">
            {lessonBlocks.map((lessonBlock) => (
                <LessonBlock key={lessonBlock.lessonNumber} lessonNumber={lessonBlock.lessonNumber} lessonStatus={lessonBlock.lessonStatus} />
            ))}
        </div>
    )
}

export default LessonBlockList;
