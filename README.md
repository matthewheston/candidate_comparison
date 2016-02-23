## Motivation

I'm trying to begin thinking about how we could use technology to help people
think about and compare political candidates. At least in presidential
elections, candidates also have an "Issues" page on their website where they
talk about issues they care about and their policy plans to address those
issues. But it's not always easy to compare what issues different candidates are
talking about and how they're talking about them. I'm interested in using
different techniques, ranging from very simple to more sophisticated, to help
voters engage in this comparative task.

## So what's here currently?

Not too much. To begin addressing this idea, I've only focused on Hillary
Clinton and Bernie Sanders. Right now you can navigate to the [Issues we
Found](issues_we_found.md) page. This was built by using some basic web scraping
to collect a list of issues that each of these candidates lists on their
website. At the bottom of that page, you'll find a table of issues where we
think there is overlap between the two candidates based on fuzzy string matching
on just the names of the issues. Each row of that table links to a page where we
compare what each candidate has to say about that issue. This isn't always
pretty. Right now we just show you bullet point text extracted on each
candidate's issue page.
