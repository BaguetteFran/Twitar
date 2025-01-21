export interface Tweet {
  id: number;
  handle: string | null;
  display_name: string | null;
  avatar: string | null;
  text_content: string | null;
  created_at: string | null;
  like_count: number | null;
  repost_count: number | null;
  reply_count: number | null;
  media: string | null;
  media_type: string | null;
  score: number | null;
}
