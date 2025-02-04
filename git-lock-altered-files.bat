@echo off
echo "Locking archive.txt"
git update-index --skip-worktree .\archive.txt
echo "Locking batchURLs.txt"
git update-index --skip-worktree .\batchURLs.txt
echo "Locking config_pods_playlist.txt"
git update-index --skip-worktree .\config_pods_playlist.txt
echo "Locking config_pods_username.txt"
git update-index --skip-worktree .\config_pods_username.txt
echo "Locking config_pods_cherrypick.txt"
git update-index --skip-worktree .\config_pods_cherrypick.txt
echo "Done. Further edits will be ignored"