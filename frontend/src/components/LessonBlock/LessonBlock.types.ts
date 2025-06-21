export enum LessonStatus {
    COMPLETED = "completed",
    IN_PROGRESS = "in-progress",
    NOT_STARTED = "not-started"
}

export interface LessonBlockProps {
  id: string;
  text: string;
  romaji: string;
  translation: string;
  audio_url: string;
  status: LessonStatus;
}
