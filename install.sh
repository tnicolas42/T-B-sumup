brew install redis

brew services start redis
brew services list | grep redis

echo "source `git rev-parse --show-toplevel`/zsh_config.zsh" >> ~/.zshrc
