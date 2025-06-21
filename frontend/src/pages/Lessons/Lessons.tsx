import LessonBlockList from "@/components/LessonBlockList/LessonBlockList"
import { LessonStatus } from "@/components/LessonBlock/LessonBlock.types"

const lessonBlocks = [
  { lessonNumber: 1, lessonStatus: LessonStatus.COMPLETED },
  { lessonNumber: 2, lessonStatus: LessonStatus.IN_PROGRESS },
  { lessonNumber: 3, lessonStatus: LessonStatus.NOT_STARTED },
  { lessonNumber: 4, lessonStatus: LessonStatus.NOT_STARTED },
  { lessonNumber: 5, lessonStatus: LessonStatus.NOT_STARTED },
]

function Lessons() {  
  return (    
    <LessonBlockList lessonBlocks={lessonBlocks} />        
  )
}

export default Lessons;