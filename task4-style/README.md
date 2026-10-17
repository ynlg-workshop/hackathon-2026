# Who Wrote This? Stylometric Fingerprinting in Story Continuation

Can writing style reveal who wrote a story continuation? Build a project that attributes text to a human author, a particular LLM, or a group of models.

The same prompt can produce very different continuations. Yet author signals can be brittle: pairwise comparison may work, while single-text attribution can approach chance, especially across prompt topics. Explore where these signals hold up and where they disappear.

## Aim

Choose a question that interests your team and make the result easy to discuss. A classifier, visualisation, error analysis, interactive demo, or a well-supported negative result all make for a good project.

## Data

### Human vs. AI

[`vkpriya/GPT-WritingPrompts`](https://huggingface.co/datasets/vkpriya/GPT-WritingPrompts) provides 97K prompts, 272K human continuations, and 206K GPT-3.5 continuations. Use it to study human-versus-AI attribution without generating new text.

### Model Attribution

[`jjrussell10/storyscope`](https://huggingface.co/datasets/jjrussell10/storyscope) contains 10K prompts, stories from GPT-5.4, Claude Sonnet 4.6, DeepSeek V3.2, Kimi K2.5, and Gemini 3 Flash, plus 304 narrative features.

StoryScope asks models to write complete stories from prompts rather than continue an existing passage, and it contains no human text. Its reported baseline reaches 68.4% macro F1 with narrative features.

### Bring Your Own Data

You can use another existing dataset, combine datasets, or create your own. [`euclaise/writingprompts`](https://huggingface.co/datasets/euclaise/writingprompts) and the filtered [`agentlans/euclaise-WritingPromptsX`](https://huggingface.co/datasets/agentlans/euclaise-WritingPromptsX) provide human continuations; generate additional continuations when you want to compare other models.

## Ideas

Use these as prompts for exploration:

- Compare stylometric features: sentence length, punctuation, vocabulary diversity, POS n-grams, dependency patterns, perplexity, or entropy.
- Test whether results transfer across topics, text lengths, paraphrases, or translations.
- Detect a switch between a human opening and an LLM ending.
- Compare simple feature-based models, fine-tuned language models, and LLM prompting.
- Make an interactive tool or visualisation that exposes differences between authors.

## Share Your Work

Bring something that shows your question, approach, and findings: a demo, notebook, script, visualisation, sample predictions, or result plot.

For attribution experiments, macro F1 works well for multiple sources and accuracy for human-versus-AI classification. Include enough context to interpret the result, such as the data split, baseline, and notable failure cases.

Focus on a clear, interesting contribution that you can present to the group.
