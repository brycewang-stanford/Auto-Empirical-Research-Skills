---
name: do-agent
description: This skill should be used when the user asks to "/do-agent", asks for "Execute complex tasks using multi-agent architecture with context protection", or needs the workflow previously provided by the /do-agent slash command.
version: 0.1.0
---

Explore and ultrathink to design a systematic multi-agent, multi-stage (up to 10 subagents in parallel in each stage) execution plan to accomplish: $ARGUMENTS

执行模式：explore → ultrathink → plan → track → execute → review → revise → deliver final output

Note:

- Get the current Date and Time (Beijing time)
- 创建临时工作目录 `agent_tasks/{short task description}_yyyyddmmhh/` 作为临时工作空间（if a folder with this name already exists, make a new one to avoid overwriting existing materals）
- When assigning tasks to subagents, specify their input and output files explicitly
- 每个子代理必须自己将处理结果立即保存到本地文件，不要返回给主代理！子代理自己马上保存，不要返回给主代理！
- 严禁将子代理完整输出返回主代理；只返回状态摘要
- 第一个本地输出文件：multi-agent execution plan 文档 `agent_tasks/{short task description}_yyyyddmmhh/plan.md`
- The main/mother agent must allow all Read + Write + Bash tools for all sub-agents
- Apply context engineering — main agent context is scarce
- The execution plan must include (at minimum) these four phases, each with multiple agents (in parallel when possible):
  1. 规划阶段：信息收集与方案规划
  2. 实施阶段：执行与整合任务结果
  3. 对任务结果进行审阅与反馈
  4. 根据审阅反馈，对任务结果进行全面修订
- Do not ask for plan approval, just set up the tasks tracking and do it once the planning phase finished
- Complete automation of the entire process, from planning to execution to review and revision, without any human intervention
