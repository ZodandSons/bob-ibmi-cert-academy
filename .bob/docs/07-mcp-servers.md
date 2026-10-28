# 07 · MCP servers: `mcp.json` and `mcp-tools/`

[Docs home](../README.md) · [← 06 Slash commands](06-slash-commands.md) · Next: [08 Hooks →](08-hooks.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 1.3, 2.13, 3.9, 4.5. Exam-focused notes: [Section 1](exam/section-1-concepts.md) · [Section 2](exam/section-2-core-features.md) · [Section 3](exam/section-3-use-cases.md) · [Section 4](exam/section-4-configuration.md).

## In plain English
On its own, Bob can only see the files in your repository. **MCP (Model Context
Protocol)** is a standard plug that lets Bob talk to outside systems through small
helper programs called **MCP servers**. Here we plug Bob into **IBM i**, so it can
answer *"which programs use CUSTMAST?"* from the live system, not by guessing from
source code.

```
 Bob ──MCP──► IBM i MCP server (runs on your PC via npx) ──Mapepire──► IBM i / Db2 for i
              reads .bob/mcp-tools/ibmi-dev-tools.yaml       (port 8076)
              = the exact list of SQL tools Bob may call
```

## Where it lives
| File | Scope |
|---|---|
| `.bob/mcp.json` | This project, shared through git |
| `~/.bob/settings/mcp.json` (Windows: `%APPDATA%\Bob\settings\mcp.json`) | You, in every project |

If both define a server with the same name, the **project** one wins. Manage servers in
the IDE's MCP settings panel, or with `/mcp` and `bob mcp list` in Bob Shell.

## Anatomy of `mcp.json`
JSON can't hold comments, so here is the file annotated:

```jsonc
{
  "mcpServers": {
    "ibmi-mcp": {                                   // server name: tools show up under it
      "command": "npx",                             // a LOCAL (stdio) server: Bob starts this process
      "args": ["-y", "@ibm/ibmi-mcp-server@latest", // IBM's open-source IBM i MCP server from npm
               "--tools", ".bob/mcp-tools/ibmi-dev-tools.yaml"],  // which SQL tools to offer
      "cwd": "${workspaceFolder}",                  // run from repo root so the relative path works
      "env": {                                      // environment for the server process
        "DB2i_HOST": "${DB2i_HOST}",                // ${VAR} = taken from YOUR environment,
        "DB2i_USER": "${DB2i_USER}",                //   so no credentials are committed
        "DB2i_PASS": "${DB2i_PASS}",
        "DB2i_PORT": "8076",                        // Mapepire's default port
        "MCP_TRANSPORT_TYPE": "stdio"
      },
      "alwaysAllow": [],                            // tool names to run without asking (empty = always ask)
      "disabled": false
    },
    "ibmi-mcp-shared": {                            // a REMOTE server, e.g. one the team runs centrally
      "type": "streamable-http",
      "url": "https://ibmi-mcp.example.internal:3010/mcp",
      "headers": { "Authorization": "Bearer ${IBMI_MCP_TOKEN}" },
      "disabled": true                              // off by default: example only
    }
  }
}
```

**Credentials:** set `DB2i_HOST`, `DB2i_USER`, `DB2i_PASS` in your shell profile before
starting Bob. In Bob Shell you can store secrets encrypted instead:
`/manage-secrets set DB2i_PASS ...` (referenced the same way, as `${DB2i_PASS}`).
IBM's own repo also shows the alternative of committing `mcp.json.example` and
git-ignoring the real `mcp.json`.

## Anatomy of a tool: `mcp-tools/ibmi-dev-tools.yaml`
Each tool is a named, parameterised SQL statement. The `description` is what Bob reads
to decide when to call it, so write it for Bob.

```yaml
tools:
  where_used:
    source: ibmi-system                 # connection defined under sources:
    description: >-                     # Bob picks tools by this text
      Impact analysis: find every program in a library that references a given
      file or program. Use before changing a file layout or a called program.
    parameters:
      - name: library                   # becomes :library in the SQL (bound, not pasted)
        type: string
        required: true
        maxLength: 10
    statement: |
      SELECT PROGRAM_LIBRARY, PROGRAM_NAME, OBJECT_TYPE, FILE_USAGE
        FROM QSYS2.PROGRAM_REFERENCES
       WHERE PROGRAM_LIBRARY = :library AND OBJECT_NAME = :object
    security:
      readOnly: true                    # the server refuses anything that writes
```

Tools in this repo: `list_objects`, `program_references`, `where_used`, `table_columns`,
`recent_job_messages`, `active_jobs_in_subsystem`. All are **read-only**.

## Which modes can use MCP?
Only modes whose `groups` include `mcp`: `rpg-dev`, `cl-dev`, `ibmi-reviewer` and `ibmi-ops`
(plus the built-in Agent, Plan and Ask). See [04 Custom modes](04-custom-modes.md).

## Setup checklist
1. On the IBM i: install and start Mapepire (`yum install mapepire-server`; see its
   [README](https://github.com/Mapepire-IBMi/mapepire-server)).
2. On your PC: Node.js installed, and `DB2i_HOST` / `DB2i_USER` / `DB2i_PASS` set.
3. Check the tools load without Bob:
   `npx -y @ibm/ibmi-mcp-server@latest --list-toolsets --tools .bob/mcp-tools`
4. Restart Bob (or toggle the server in MCP settings). `bob mcp list` should show `ibmi-mcp`.
5. In **📊 IBM i Ops Analyst** mode: *"List the programs in ORDDEV01."*

## Try it: add your own tool
Append to `ibmi-dev-tools.yaml`:
```yaml
  data_area_value:
    source: ibmi-system
    description: Read the current value of a data area.
    parameters:
      - { name: library, type: string, required: true }
      - { name: data_area, type: string, required: true }
    statement: |
      SELECT DATA_AREA_VALUE FROM QSYS2.DATA_AREA_INFO
       WHERE DATA_AREA_LIBRARY = :library AND DATA_AREA_NAME = :data_area
    security: { readOnly: true }
```
Add it to the `toolsets` list, restart the server, and ask Bob for a data area value.

## Tips and common mistakes
- **Keep tools read-only** unless you really need writes, and then put them in a separate
  toolset that only a dedicated mode uses.
- **Write descriptions with examples** ("e.g. '123456/QUSER/ORDNIGHT'"). They are Bob's only guide.
- Leave `alwaysAllow` empty while learning, so you see every call Bob makes.
- Server not starting? Run the `npx` command from step 3 in a terminal; the error is usually there.

**Docs:** [MCP in Bob (IDE)](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-in-bob) ·
[Understanding MCP](https://bob.ibm.com/docs/ide/configuration/mcp/understanding-mcp) ·
[Server transports](https://bob.ibm.com/docs/ide/configuration/mcp/server-transports) ·
[MCP OAuth](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-oauth) ·
[MCP in Bob Shell](https://bob.ibm.com/docs/shell/configuration/mcp/mcp-bobshell) ·
[Build MCP servers with Bob (tutorial)](https://bob.ibm.com/docs/ide/tutorials/mcp-server-integration) ·
[MCP integration with IBM Bob (IBM tutorial)](https://www.ibm.com/think/tutorials/mcp-integration-ibm-bob)

**IBM repos:** [IBM/ibmi-mcp-server](https://github.com/IBM/ibmi-mcp-server) (server,
tool schema in `tools/README.md`, example tools in `tools/`, and its own
[`.bob` folder](https://github.com/IBM/ibmi-mcp-server/tree/main/.bob)) ·
[Mapepire-IBMi/mapepire-server](https://github.com/Mapepire-IBMi/mapepire-server)
