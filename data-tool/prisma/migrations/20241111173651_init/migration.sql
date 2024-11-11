-- CreateTable
CREATE TABLE "tweets" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "screen_name" TEXT,
    "profile_img" TEXT,
    "verified" INTEGER,
    "text" TEXT,
    "img_url" TEXT,
    "media" TEXT,
    "favorite_count" INTEGER,
    "view_count" INTEGER,
    "retweet_count" INTEGER,
    "score" INTEGER
);

-- CreateIndex
CREATE UNIQUE INDEX "tweets_id_key" ON "tweets"("id");
