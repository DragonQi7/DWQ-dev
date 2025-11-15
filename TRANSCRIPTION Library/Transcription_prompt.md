### ChatGPT prompt — Organize lecture transcription with timestamps

Use the prompt below. Replace bracketed fields before sending and paste the full transcript where indicated.

Prompt:
---
You are an expert editor and lecture summarizer. Given the raw transcription below, produce a clean, navigable, and fully referenced lecture digest that preserves detail, groups content by topic, and shows exactly when important points occur in the recording.

Inputs (replace as needed):
- Transcript: <<<PASTE TRANSCRIPT TEXT HERE>>>  
- Timestamp format in transcript: <<<e.g., [00:02:15], 00:02:15, or none>>>  
- Speakers labeled in transcript: <<<Yes / No; if Yes, give label format e.g., "Speaker 1:" or "Dr. Stone:">>>  
- Desired time granularity for references: <<<e.g., HH:MM:SS, MM:SS, or minute only>>>  
- Maximum summary length per section: <<<e.g., 2–4 sentences>>>  
- Special instructions (optional): <<<e.g., preserve direct quotes; create glossary; flag unclear audio; include CSV appendix>>>  

Required outputs and structure:
1. Title block: one-line lecture title (from transcript or create), speaker(s), date (if present), total duration (estimate if not present).  
2. At-a-glance: 3–5 bullet “most important takeaways” with timestamps.  
3. Structured topics: divide the lecture into topical sections. For each section include:
   - Section heading (topic phrase).  
   - Time range (start–end) using the chosen granularity.  
   - Concise summary (use the provided max length).  
   - Key points as a short numbered list; each key point ends with the timestamp where it appears.  
   - Important verbatim quote(s) (if present) with timestamp(s).  
4. Full timeline: chronological short-paragraph timeline of every major idea or transition with timestamps (use bullets or numbered list).  
5. Speaker map: list speakers, one-line role description, and notable timestamps for when they speak.  
6. Glossary / definitions: list technical terms introduced, one-line definition each, and the timestamp where first mentioned.  
7. Unclear audio or gaps: list any timestamps showing “[inaudible]” or unclear text.  
8. Searchable index: alphabetized list of 10–30 keywords/topics with 1–2 timestamps each where they appear.  
9. Optional appendices (only if requested in Special instructions): full cleaned transcript with standardized timestamps, or a CSV-ready table of sections with start/end times and 1-line summaries.

Formatting and quality rules:
- Use exact timestamps from the transcript; if none exist, create estimates and label them “[estimated timestamp]”.  
- Keep language neutral, professional, and concise.  
- Preserve factual detail; do not add claims not present in the transcript.  
- When paraphrasing, retain original meaning; if uncertain, mark with “[paraphrase — check audio]”.  
- If speaker labels are missing, infer turns as Speaker A, Speaker B, etc., and note these are inferred.  
- Use the requested time granularity consistently across the output.

If the transcript exceeds your input capacity, process it in sequential chunks, produce this format for each chunk, and then merge into one consolidated digest preserving original timestamps.

Now: read the Transcript input above and produce the requested digest following every rule and section described.

--
rewrite millionare feng shui notes.txt and format it correctly. but the re-written notes in a md file.
do not reword theoriginal wording and don't add any outside information to the rewrite
make sure there are headers and guidelines to each rewritten sections

