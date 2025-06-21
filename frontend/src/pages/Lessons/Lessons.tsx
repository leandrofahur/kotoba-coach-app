import { useQuery } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";

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
  const getLessons = async () => {
    const response = await fetch("http://localhost:8000/api/v1/phrases");
    const data = await response.json();
    return data;
  }

  const { data: lessons, isLoading } = useQuery({
    queryKey: ["lessons"],
    queryFn: () => getLessons()
  });


  return (          
    <div className="w-full flex flex-col space-y-3 items-center justify-center h-screen bg-white p-4 gap-4">
      {isLoading ? (
        <div className="flex flex-col space-y-3 items-center justify-center h-screen p-4 gap-4">
          <Skeleton className="h-[80px] w-[250px] rounded-xl" />
          <Skeleton className="h-[80px] w-[250px] rounded-xl" />
          <Skeleton className="h-[80px] w-[250px] rounded-xl" />
          <Skeleton className="h-[80px] w-[250px] rounded-xl" />
          <Skeleton className="h-[80px] w-[250px] rounded-xl" />
          <Skeleton className="h-[80px] w-[250px] rounded-xl" />
        </div>
      ) : (
        <LessonBlockList lessonBlocks={lessons} />
      )}
    </div>    
  )
}

export default Lessons;