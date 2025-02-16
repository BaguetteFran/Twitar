export interface Tweet {
    id: string;
    created_at: string | null;
    screen_name: string | null;
    profile_img: string | null;
    verified: number | null;
    text: string | null;
    media: string | null;
    urls: string | null;
    thumbnail: string | null;
    favorite_count: number | null;
    view_count: number | null;
    retweet_count: number | null;
    score: number | null;
  }