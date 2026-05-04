#!/usr/bin/env bash
# wiki-mcp-watchdog.sh — 监控 wiki MCP 健康状态，异常时触发 hermes-gateway 重启
# 用法: 加入 crontab，每 5-10 分钟执行一次
# crontab -e 添加: */10 * * * * /home/gyt/Documents/Functional_projects/wiki-cli/scripts/wiki-mcp-watchdog.sh >> /tmp/wiki-mcp-watchdog.log 2>&1

set -euo pipefail

LOG="/tmp/wiki-mcp-watchdog.log"
GATEWAY_PID=$(pgrep -f "hermes.*gateway" | head -1 || true)
WIKI_MCP_PID=$(pgrep -f "wiki.*mcp" | head -1 || true)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

log "=== Watchdog run ==="
log "Gateway PID: ${GATEWAY_PID:-none}"
log "Wiki MCP PID: ${WIKI_MCP_PID:-none}"

# 健康检测：用 wiki stats CLI 测试（15s 超时）
health_check() {
    timeout 15 /home/gyt/anaconda3/envs/mineru/bin/wiki stats \
        --path /mnt/o/Nanashi/Documents/Wiki/paper-wiki \
        > /dev/null 2>&1
}

if health_check; then
    log "✓ Wiki CLI healthy"
    exit 0
fi

log "⚠️ Wiki CLI unhealthy — sending USR1 to gateway (pid=$GATEWAY_PID) to trigger reload..."

if [ -n "$GATEWAY_PID" ]; then
    kill -USR1 "$GATEWAY_PID" 2>/dev/null || true
    log "Sent USR1, waiting 10s for reconnect..."
    sleep 10
else
    log "No gateway PID found, skipping restart signal"
fi

# 验证恢复
if health_check; then
    log "✓ Wiki CLI recovered after restart signal"
else
    log "✗ Wiki CLI still unhealthy after restart signal"
fi
