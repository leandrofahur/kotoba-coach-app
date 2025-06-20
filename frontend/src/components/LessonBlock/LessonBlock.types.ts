export enum LessonStatus {
    COMPLETED = "completed",
    IN_PROGRESS = "in-progress",
    NOT_STARTED = "not-started"
}

export interface LessonBlockProps {
  lessonNumber: number;  
  lessonStatus: LessonStatus;
}
