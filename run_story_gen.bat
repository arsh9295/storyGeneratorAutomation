@echo off
call sgvenv\Scripts\activate
cd /d F:\AI_2\storyGeneratorAutomation\UI
@python.exe story_generator_gui.py %*
@pause