@echo off
echo "Unlocking archive.txt"
git update-index --no-skip-worktree .\archive.txt
echo "Unlocking batchURLs.txt"
git update-index --no-skip-worktree .\batchURLs.txt
echo "Unlocking config_pods_playlist.txt"
git update-index --no-skip-worktree .\config_pods_playlist.txt
echo "Unlocking config_pods_username.txt"
git update-index --no-skip-worktree .\config_pods_username.txt
echo "Unlocking config_pods_cherrypick.txt"
git update-index --no-skip-worktree .\config_pods_cherrypick.txt
echo "Done. Files cleared to commit"