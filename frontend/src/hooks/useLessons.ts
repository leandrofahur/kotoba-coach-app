import { useQuery } from "@tanstack/react-query";
import type { LessonBlockProps } from "@/components/LessonBlock/LessonBlock.types";

export const useLessons = () => {
  return useQuery<LessonBlockProps[]>({    
    queryKey: ["lessons"],
    queryFn: async () => {
      const response = await fetch("http://localhost:8000/api/v1/phrases");
      return response.json();
    }
  });
};

export const useLesson = (id: string) => {
  return useQuery<LessonBlockProps>({
    queryKey: ["lesson", id],
    queryFn: async () => {
      const response = await fetch(`http://localhost:8000/api/v1/phrases/${id}`);
      return response.json();
    },
    enabled: !!id
  });
}; 