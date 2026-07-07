#!/usr/bin/env node

async function main() {
  const chunks = [];

  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  let payload = {};

  try {
    payload = JSON.parse(Buffer.concat(chunks).toString());
  } catch (err) {
    console.error("Invalid hook payload:", err.message);
    process.exit(1);
  }

  const tool = payload.tool_name || "";
  const input = payload.tool_input || {};

  const readPath =
    input.AbsolutePath ??
    input.SearchPath ??
    input.file_path ??
    input.filename ??
    input.path ??
    "";

  // Check if tool name is relevant or if the file read ends with .env
  const toolLower = tool.toLowerCase();
  const isReadOrGrep =
    toolLower.includes("read") ||
    toolLower.includes("grep") ||
    toolLower.includes("view");

  const isEnvFile =
    readPath.endsWith(".env") ||
    readPath.includes(".env/") ||
    readPath.includes(".env\\") ||
    readPath === ".env";

  if (isReadOrGrep && isEnvFile) {
    console.log(
      JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: "Reading .env files is not allowed."
        }
      })
    );
    process.exit(0);
  }

  // Otherwise allow
  console.log(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "allow"
      }
    })
  );
  process.exit(0);
}

main();
