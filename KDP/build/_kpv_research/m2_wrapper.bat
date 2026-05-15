@echo off
"C:\Users\apart\AppData\Local\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe" -convert "E:\Projects\BookBlogsHome\LLMBook\KDP\build\_kpv_research\m2_sched.epub" -output "E:\Projects\BookBlogsHome\LLMBook\KDP\build\_kpv_research\m2_sched.kpf" -qualitychecks > "E:\Projects\BookBlogsHome\LLMBook\KDP\build\_kpv_research\m2_sched.stdout.log" 2> "E:\Projects\BookBlogsHome\LLMBook\KDP\build\_kpv_research\m2_sched.stderr.log"
echo rc=%ERRORLEVEL% > "E:\Projects\BookBlogsHome\LLMBook\KDP\build\_kpv_research\m2_sched.rc.log"
