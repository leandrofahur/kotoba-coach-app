export const LessonStatus = {
    COMPLETED: "completed",
    IN_PROGRESS: "in-progress",
    NOT_STARTED: "not-started"
} as const;

export type LessonStatus = typeof LessonStatus[keyof typeof LessonStatus];

export interface LessonBlockProps {
  id: string;
  text: string;
  romaji: string;
  translation: string;
  audio_url: string;
  status: LessonStatus;
}
