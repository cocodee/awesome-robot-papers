<!-- Retrieved 2026-10-22; converted with scripts/convert_to_markdown.py. Site-relative links resolved to the original site; embedded charts archived separately in assets/natura-1/. Videos are not archived. -->

[Skip to article](https://www.naturewill.com/blog/natura-1?lang=en#article-reading)

[![Nature Will](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/a4adb.svg)](https://www.naturewill.com/?lang=en#main)
[Research](https://www.naturewill.com/blog/natura-1?lang=en)[Career](https://www.naturewill.com/career?lang=en)[About Us](https://www.naturewill.com/about?lang=en)

[English](https://www.naturewill.com/blog/natura-1?lang=en)[简体中文](https://www.naturewill.com/blog/natura-1?lang=zh-CN)

# The Will to *Act.*

Introducing Natura-1:
Scaling general dexterous manipulation through human experience

1. [(1)Introducing Natura-1](https://www.naturewill.com/blog/natura-1?lang=en#introduction)
2. [(2)Everything Has to Scale](https://www.naturewill.com/blog/natura-1?lang=en#the-case)
3. [(3)Real-World Capabilities](https://www.naturewill.com/blog/natura-1?lang=en#real-world)
4. [(4)Built to Scale](https://www.naturewill.com/blog/natura-1?lang=en#built-to-scale)
5. [(5)The Work Ahead](https://www.naturewill.com/blog/natura-1?lang=en#outlook)

[Scroll](https://www.naturewill.com/blog/natura-1?lang=en#article-reading)

[The Will to Act. ↑](https://www.naturewill.com/blog/natura-1?lang=en#article-title)

1. [1Introducing Natura-1](https://www.naturewill.com/blog/natura-1?lang=en#introduction)
2. [2Everything Has to Scale](https://www.naturewill.com/blog/natura-1?lang=en#the-case)
3. [3Real-World Capabilities](https://www.naturewill.com/blog/natura-1?lang=en#real-world)
   1. [3.1Benchmarking dexterous manipulation](https://www.naturewill.com/blog/natura-1?lang=en#heading-benchmark "Benchmarking dexterous manipulation")
   2. [3.2Long-horizon execution with dexterous hands](https://www.naturewill.com/blog/natura-1?lang=en#heading-demos "Long-horizon execution with dexterous hands")
   3. [3.3Zero-shot generalization and instruction following](https://www.naturewill.com/blog/natura-1?lang=en#heading-instruction "Zero-shot generalization and instruction following")
   4. [3.4Emergent behaviors beyond predefined capabilities](https://www.naturewill.com/blog/natura-1?lang=en#heading-observations "Emergent behaviors beyond predefined capabilities")
4. [4Built to Scale](https://www.naturewill.com/blog/natura-1?lang=en#built-to-scale)
   1. [4.1Data](https://www.naturewill.com/blog/natura-1?lang=en#subsection-data "Data")
   2. [4.2Infrastructure](https://www.naturewill.com/blog/natura-1?lang=en#subsection-infrastructure "Infrastructure")
   3. [4.3Model](https://www.naturewill.com/blog/natura-1?lang=en#subsection-model "Model")
5. [5The Work Ahead](https://www.naturewill.com/blog/natura-1?lang=en#outlook)

Natura-1 is our first general foundation model for the physical world. It is a single model that follows plain language instructions zero-shot and carries them out with dexterous hands.

![Your browser does not support video.](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/natura-1/local/posters/hero-collage-20261013.webp)

1

## Introducing Natura-1

**At Nature Will, our mission is to solve general physical intelligence**, building foundation models that learn directly from human experience, master general dexterous manipulation, and generalize across the physical world. That physical world was shaped by and for the human hand: we made tools to fit our hands, then used those tools to make everything else. In such a world, no machine can be truly general without being dexterous.

Yet enabling a general foundation model to control high-degree-of-freedom (DoF) dexterous hands remains a major challenge in physical intelligence. Contact dynamics leave little room for error, and the action space grows exponentially with the number of hand joints. As a result, prior work has largely focused on either general-purpose policies for simple grippers or task-specific systems for dexterous manipulation.

**Today, we are introducing Natura-1, our first general foundation model for the physical world.** Natura-1 is a 50-billion-parameter mixture-of-experts (MoE) model pretrained on more than one million hours of egocentric human experience. It takes in language and vision and drives 20-DoF dexterous hands within a 100-millisecond control loop. On top of this foundation, we conduct efficient post-training on a limited amount of robot data to adapt pretrained world knowledge to dexterous manipulation, yielding a model that generalizes to a wide range of unseen scenarios. Natura-1 follows complex natural-language instructions zero-shot, reasoning through spatial constraints, multi-object relationships, and negative conditions. It can also autonomously carry out long, continuous workflows, including folding delicate, deformable materials, rendering calligraphy with compliant brushstrokes, and switching tools on the fly across multi-stage tasks.

Together, these results offer early evidence that a single foundation model can learn dexterous skills from human experience and apply them to unfamiliar tasks and environments. Rather than engineering a separate solution for every task, we aim to expand these capabilities by learning from human experience **at greater scale**.

2

## Everything Has to Scale

**A general model is only as general as its experience.** The physical world is too varied to be covered by designed tasks or hand-built skills, so the goal is simple to state: train a very large model, using substantial computing resources, with data that spans as many environments and tasks as possible. Larger models and more compute are not enough. To generalize across the physical world, a model needs experience as varied as the world itself.

Before building anything, we therefore asked where physical experience exists at this scale. At present, robots cannot provide it. Robot data collection is bounded by robot capability: a robot can only gather data in settings where it already works, and it can only work in settings where data already exists. Humans, by contrast, already operate across virtually every environment and task, with their hands central to much of that activity. This is why Natura-1 learns from human experience, and why it is designed for dexterous hands.

Training on human data at this scale required building the full stack in-house. Our data infrastructure manages tens of petabytes in a unified lakehouse, with a throughput of hundreds of thousands of hours of egocentric video per week. It deduplicates footage at both the video and clip level across all sources, and screens for visual and sensor anomalies. It also enforces per-task quotas that keep the distribution close to real human activity. We then recover dense 3D hand poses from monocular and stereo video. Each activity is annotated hierarchically, from its overall goal down to subtasks and individual steps. While no robot hand maps exactly onto the human hand, anthropomorphic dexterous hands offer the closest correspondence available today. After filtering, the curated corpus comprises one million hours of language-conditioned action trajectories.

We train on this data with an in-house distributed engine co-designed with a 50-billion-parameter mixture-of-experts (MoE) architecture, developed to unify visual world modeling and action generation. Batches stream directly from object storage without relying on a shared file system, and custom attention kernels considerably outperform general baselines such as FlexAttention on our workloads. The stack sustains over 50% Model FLOPs Utilization (MFU) across long-running jobs on hundreds of GPUs. Following pretraining, a limited amount of robot manipulation data is sufficient to adapt the model to a physical robot hand. At inference, a Rust orchestrator layer overlaps observation streaming, computation, and action transfer, while fused CUDA kernels trim latency on the critical path. Together, they maintain a strict 100-millisecond observation-to-action loop on physical hardware. Natura-1 is among the first models trained on this stack, and each of its components has been designed to ***scale further.***

> Every video and every result that follows comes from a single foundation model: Natura-1.[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

† Six long-horizon tasks, marked †, use additional tuning on top of Natura-1; all other results share the same weights.

3

## Real-World Capabilities

We evaluate Natura-1 on physical dual-arm robots with dexterous hands. We begin with a benchmark that measures dexterous manipulation along twelve capability dimensions. We then test how precisely, and for how long, a single policy can carry out multi-step tasks without human intervention. These tasks last several minutes and require both fine hand control and coordinated action from start to finish. Next we test zero-shot generalization: whether Natura-1 can follow open-ended language instructions on tasks it was never trained to perform. The last part covers something we did not plan to measure at all: actions the model came up with on its own when a task did not go as expected.

Taken together, these results show that a single foundation model can be both dexterous and general. They also give an early glimpse at physical capabilities that emerge at scale without being designed in.

### 3.1Benchmarking dexterous manipulation

The absence of a publicly recognized dexterous-hand foundation model makes a strictly like-for-like baseline unavailable, so we select two representative baselines spanning different paradigms: π0.5, a well-established vision-language-action (VLA) foundation model, and GPT-6-Astra, a frontier large multimodal model that we use directly as a coding-based policy. On our dual-arm platform (ROKAE AR5 with Wuji hands), neither baseline produces a scored result: π0.5 fails even after being fine-tuned on our dexterous-hand robot data, and GPT-6-Astra fails to score within the 60-minute per-task time limit. We also evaluate both baselines on the ARX AC One dual-arm gripper platform, first fine-tuning π0.5 on gripper demonstrations covering exactly the same general tasks as Natura-1's dexterous-hand training set. Under this setting, π0.5 and GPT-6-Astra score 13.5 and 16.7 with grippers, respectively, whereas Natura-1 scores **53.4 (Base)** and **59.1 (Agentic)** with 20-DoF dexterous hands.

The four tasks below illustrate the principle behind the benchmark: none of them appears in Natura-1's post-training data, and neither do their scenes, objects, or action combinations. All evaluations use a single fixed training set of real-robot trajectories, with no task-specific tuning for these tasks; every result therefore reflects generalization rather than recall. Each execution is shown alongside the closest demonstrations retrieved from the training set, allowing readers to understand the benchmark's design and judge how much each task differs from the model's training experience.

THE ANATOMY OF GENERALIZATION

01 / 04←→

![](https://media.naturewill.com/research-blog/media/v011-cefdd677/20261012T210313Z-089ca3c35ad7/cover.webp)0:33Tray loading & transport![](https://media.naturewill.com/research-blog/media/v017-d03ef707/20261012T210313Z-089ca3c35ad7/cover.webp)0:18Extract, wipe, and dispose![](https://media.naturewill.com/research-blog/media/v015-3c681117/20261012T210313Z-089ca3c35ad7/cover.webp)0:45Adding sugar & stirring![](https://media.naturewill.com/research-blog/media/v012-295d2efd/20261012T210313Z-089ca3c35ad7/cover.webp)0:51Preparing a pot

BENCHMARK TASK 01 / 04

#### Tray loading & transport

0:33 FILM

Compositional GeneralizationTool & Object GeneralizationSpatial & Scene Generalization

Natura-1 · ZERO-SHOT EXECUTION

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v011-cefdd677/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:01Place apple in bowl0:12Seat bottle upright on tray0:23Carry the loaded tray

RETRIEVED TRAINING RELATIVES

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v010-d8e828de/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

##### Picking and placing a fruit

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v009-f5695719/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

##### Carrying a loaded tray

Instruction: Place the red apple in the blue bowl, set the pink bottle on the tray, and carry the loaded tray to the blue placemat.

Natura-1 places the items on the middle tray and carries it with both arms without moving the tray beside it. The training examples show separate actions, such as picking up a fruit and carrying a tray that is already loaded. Here, the model generalizes to grasping the bottle and combines these actions in a different table layout. It also keeps the loaded tray balanced and avoids the tray beside it.

BENCHMARK TASK 02 / 04

#### Extract, wipe, and dispose

0:18 FILM

Spatial & Scene GeneralizationNew-Action Generalization

Natura-1 · ZERO-SHOT EXECUTION

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v017-d03ef707/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:02Pull out a tissue0:06Wipe away the water0:12Discard the tissue

RETRIEVED TRAINING RELATIVES

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v018-29b60e35/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

##### Taking and placing a tissue

Instruction: Pull a tissue from the box, wipe the wet area beside the cup, and drop the used tissue into the bin.

Natura-1 pulls out a tissue, wipes the wet area beside the cup, and drops the used tissue into the bin. The training example shows only pulling a tissue from a box and placing it on a tray. Here, the model uses the tissue to clean, adjusting pressure as it wipes. It finds the box, wet area, and bin in a different table layout and moves around the cup without disturbing it.

BENCHMARK TASK 03 / 04

#### Adding sugar & stirring

0:45 FILM

Spatial & Scene GeneralizationTool & Object Generalization

Natura-1 · ZERO-SHOT EXECUTION

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v015-3c681117/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:03Add sugar to the cup0:36Pick up the straw0:40Stir with the straw

RETRIEVED TRAINING RELATIVES

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v016-12e013db/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

##### Beaker stirring with glass rod

Instruction: Scoop a spoonful of white sugar into the pink cup, pick up the straw, and stir the liquid with it.

Natura-1 adds the sugar, returns the spoon, and uses the straw to stir inside the narrow cup. Training shows stirring with a thin glass rod in a wide laboratory beaker. Here, Natura-1 transfers that skill to a wider plastic straw and a narrow ceramic cup on a white test table. It also adds sugar, a step absent from the training example, adapting to new tools, objects, and surroundings.

BENCHMARK TASK 04 / 04

#### Preparing a pot

0:51 FILM

Compositional GeneralizationSpatial & Scene GeneralizationTool & Object GeneralizationNew-Action Generalization

Natura-1 · ZERO-SHOT EXECUTION

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v012-295d2efd/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Add peppercorns0:10Peel off the film0:18Pour into the pot0:42Cover the pot

RETRIEVED TRAINING RELATIVES

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v013-9f4cf191/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

##### Scooping with a spoon

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v014-28707a67/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

##### Placing an object and covering the pot

Instruction: Add a spoonful of peppercorns to the pot, peel the film off the small bowl, pour its contents into the pot, and cover the pot.

Natura-1 first adds peppercorns to the pot, then removes the film, pours in the ingredients, and puts on the lid. The training examples show scooping grains with a spoon and putting a lid on a pot. Here, the model generalizes to peeling film and pouring from a bowl, combining these actions with familiar skills in a different kitchen setup. It adjusts how it pulls the film and tilts the bowl while locating the objects needed for each step.

### 3.2Long-horizon execution with dexterous hands

While the benchmark evaluates capabilities separately, real-world tasks require them to work together in one continuous workflow. Everyday work involves more than picking and placing rigid objects: soft materials change shape, elastic parts spring back, and tools demand steady, carefully controlled pressure. Grippers can handle some of these tasks with specialized fixtures or attachments, but dexterous hands offer greater flexibility. The palm can support soft materials, the web between the thumb and index finger stabilizes tool handles, and the fingers can adjust their grip, hold elastic parts in place, and coordinate handoffs. As these actions change an object's shape, how it is supported, and its contact conditions, the model must continually adjust its grip and motion based on feedback rather than follow a fixed trajectory.

With task-specific tuning, Natura-1 demonstrates sustained autonomous execution across workflows that combine precise manipulation with multi-step coordination. The six demonstrations below show continuous, single-take autonomous workflows, several lasting multiple minutes without human intervention. Each requires a single policy to handle diverse materials and changing contact conditions, including pouring liquids, scooping items, handling flexible objects, using various tools, and precisely aligning parts.

WORKFLOW 01 / 06

#### Making wontons[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v002-05981bd1/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Separate a wrapper from the stack0:14Add filling to the wrapper0:33Fold and seal the wrapper1:05Place the wonton on a plate

#### Supporting a soft wrapper while shaping it

A wonton wrapper changes shape with contact. The hands must support the thin sheet and filling while leaving the edges free to fold. Natura-1 separates one wrapper from the stack, cups its left palm beneath it, and adds filling with a long-handled tool in its right hand. After setting down the tool, Natura-1 uses both hands to fold and seal the wrapper, then places the wonton on a plate. It adjusts how its hands support and press the wrapper as its shape changes, applying enough pressure to close the edges without tearing the wrapper or squeezing out the filling.

WORKFLOW 02 / 06

#### Packing a shipping box[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v003-39f7658f/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Pack the box0:46Fold the flaps0:59Tape the box1:46Apply the label2:08Scan the barcode

#### Coordinating both hands to hold springy flaps shut, pull and cut tape.

Natura-1 puts a layer of raffia in an open shipping box, places a soft plush item and a book inside, then adds more raffia. It adjusts its grip for each material, from loose raffia to the soft item and the book. It then folds down the box’s top flaps and tapes them shut. Both hands must work together: one holds the flaps down while the other pulls the tape tight and presses it onto the box. To cut the tape, Natura-1 adjusts the tape dispenser’s angle and presses firmly enough to cut without pulling up the attached tape or moving the box. The other hand keeps the flaps from springing open during this step. Natura-1 then uses its fingertips to carefully pinch the label coming out of the label printer and presses it onto the box. Finally, it scans the barcode with a handheld scanner.

WORKFLOW 03 / 06

#### Serving tea[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v005-29070e8e/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Scoop tea leaves0:23Pour hot water0:43Lift the cover0:52Pick up a snack1:11Replace the cover1:20Pour tea

#### Adjusting grip, angle, and pressure to pour steadily, grasp a small knob, and handle delicate food.

Natura-1 uses a spoon to scoop up tea leaves and pour them accurately into a tea funnel. After adding the leaves, it lifts the kettle by its handle and controls the angle to pour hot water steadily. To reach the snacks, Natura-1 uses its fingertips to pinch the small, smooth handle on the glass cover and lift it off the plate. With the cover removed, it uses food tongs to pick up a snack, then puts the cover back before pouring tea from a small metal teapot into tea cups. Each step requires a different way of holding and moving objects: keeping the pot steady while pouring, placing its fingertips accurately around the cover’s handle, and squeezing the tongs firmly enough to prevent slipping without crushing the food.

WORKFLOW 04 / 06

#### Chinese calligraphy[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

![Your browser does not support this video.](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/natura-1/local/posters/ch3-refresh-20261012/demo-04-main-3s.jpg)Retry video ↻

0:00Hold the brush0:08Dip into ink0:18Start writing0:35Turn the brush

#### Coordinating both hands during writing, with precise finger movements to rotate the brush in hand.

Natura-1 dips a brush into ink and starts writing on rice paper. Small changes in pressure change how much the soft brush tip spreads, so one hand must carefully control how it moves and presses the brush. The other hand holds the thin paper in place as the brush pulls against it, without causing folds or tears. Natura-1 tries to make thicker and thinner strokes by adjusting pressure as both hands work together, though writing well with a brush remains difficult. At the end, it turns the brush in its hand. This requires careful finger control to move the handle while keeping it steady and preventing it from slipping.

WORKFLOW 05 / 06

#### Applying a screen protector[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v006-047e331a/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Clean the screen0:30Place the frame0:38Press into place1:28Pull out the backing1:38Press the edges2:52Remove the frame

#### Carefully aligning the frame and removing the backing without shifting the film.

Natura-1 cleans the screen with a cloth, then carefully places a frame holding the screen protector over the phone. The frame fits tightly around the phone, so even a slight tilt can prevent it from fitting. Natura-1 lines up the edges and gently presses the frame into place, then holds the phone and frame steady against a fixed support while carefully pulling out the backing. This requires close control of the pulling angle and force to avoid moving the frame or shifting the film. Once the backing is removed, Natura-1 carefully presses along the edges and corners, adjusting fingertip pressure to push out air bubbles and help the film stick without moving it out of place.

WORKFLOW 06 / 06

#### Making a yogurt bowl[†](https://www.naturewill.com/blog/natura-1?lang=en#footnote-post-training)

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v007-37cc29fb/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Pour oats0:40Slice the banana0:58Add banana slices1:21Add fruit1:56Pour yogurt

#### Controlling the knife and keeping the plate steady while lifting, passing, and tilting it.

Natura-1 pours an open bag of oats into the bowl, then holds a banana steady on a cutting board and slices it with a knife. It adjusts the holding pressure and cutting force to keep the banana in place. Natura-1 then lifts the plate holding the banana slices and passes it to the other hand, keeping the plate steady so the slices do not slide off. It then tilts the plate to slide the slices into the bowl. After adding fruit from a fruit bowl, Natura-1 pours the thick yogurt into the bowl.

SIX COMPLETE WORKFLOWS

01 / 06←→

![](https://media.naturewill.com/research-blog/media/v002-05981bd1/20261012T210313Z-089ca3c35ad7/cover.webp)1:12Making wontons†![](https://media.naturewill.com/research-blog/media/v003-39f7658f/20261012T210313Z-089ca3c35ad7/cover.webp)2:21Packing a shipping box†![](https://media.naturewill.com/research-blog/media/v005-29070e8e/20261012T210313Z-089ca3c35ad7/cover.webp)1:42Serving tea†![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/natura-1/local/posters/ch3-refresh-20261012/demo-04-main-3s.jpg)0:50Chinese calligraphy†![](https://media.naturewill.com/research-blog/media/v006-047e331a/20261012T210313Z-089ca3c35ad7/cover.webp)3:01Applying a screen protector†![](https://media.naturewill.com/research-blog/media/v007-37cc29fb/20261012T210313Z-089ca3c35ad7/cover.webp)2:20Making a yogurt bowl†

### 3.3Zero-shot generalization and instruction following

In this section, we set aside the structure of the benchmark and test Natura-1 zero-shot on open-ended instructions. Every trial below was recorded during our researchers' day-to-day interactions with the robot: spontaneous, unscripted prompts, many of them deliberately extreme, with no reference trajectories to guide execution. The actions, manipulation strategies, objects, and scene backgrounds all differ from anything in Natura-1's robot training data. Many of the tasks are unusual even by everyday standards: objects used and arranged in unconventional ways, instructions that exclude certain choices, and physical disturbances throughout execution.

The two preceding sections test complementary properties. The long-horizon workflows demonstrate the depth of a trained skill: how precise and how sustained execution can become after task-specific tuning. The benchmark establishes zero-shot physical generalization under controlled conditions. Real-world instruction following depends on the latter. When people give a robot instructions in their own words, they will naturally ask it to handle unfamiliar objects, arrangements, and physical challenges. A policy that cannot generalize physically to such conditions fails before instruction following even begins. The question in this section is whether that generalization holds without the guardrails of a structured benchmark, when the language is open and the task unconstrained.

In these trials, language defines the goal, and real-world feedback guides the motion. When objects move, contact conditions change, or execution is disrupted, Natura-1 adjusts its actions and continues to pursue the instructed goal rather than abandoning it. This demonstrates closed-loop instruction following beyond fixed scenes and familiar routines.

**Together or in sequence****A block in a drawer****Choosing a bottle by ruling out colors****Beans into a coconut****Locating moving objects under interference****Tracking a moving lemon****Passing a tissue****Stacking boxes and blocks****Stack cups, orange & a tissue****An orange in the fold**

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v041-14fe0f92/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Grasp the toothbrush case with your left hand and the water bottle with your right hand, then put both in the bin at the same time.

##### Left hand first

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v040-ff4989a6/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: First use your left hand to pick up the toothbrush case and put it in the bin, then use your right hand to pick up the water bottle and put it in the bin.

##### Right hand first

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v042-4defd9de/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: First use your right hand to pick up the water bottle and put it in the bin, then use your left hand to pick up the toothbrush case and put it in the bin.

#### Simultaneous action or either hand order

Natura-1 regulates the limb coordination of its arms purely through language, as evidenced across three contrasting trials with a toothbrush case, a small beverage bottle, and a bin. When directed to clear the items in sequence, specifying either left-hand or right-hand priority, the robot strictly respects the temporal constraint and serializes execution. More remarkably, asking a robot to retrieve and transport two distinct objects simultaneously is an uncommon request. Yet Natura-1 faithfully adheres to the prompt. By translating verbal constraints directly into either sequential steps or simultaneous bimanual execution, Natura-1 shows high-fidelity instruction following.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v038-389cfea6/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Place a block in the open top drawer, then close the drawer.

#### Placing a block in a drawer, then steadying the cabinet to close it.

Natura-1 follows the user's instruction to pick up a wooden block and place it into the open top drawer of a small cabinet. Then, moving to close the drawer, it faces a tight space where trying to grip the edges or hook a thumb risks colliding with the cabinet frame. Reasoning through these spatial constraints, Natura-1 figures out an effective solution: it uses the tips of its four fingers to poke the drawer inward, pressing it smoothly until it sits flush against the cabinet.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v023-8a0dca54/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Pick up and hand me a bottle that is not blue, pink, orange, green, yellow, or purple.

#### Choosing the right bottle from what the instruction rules out.

The instruction rules out six colors without directly naming the bottle to choose. Natura-1 must compare the bottles on the table with all six color conditions and work out which one matches the request. It then carefully picks up the small bottle and hands it to the person.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v024-2b3fe4c9/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Scoop a spoonful of beans into the coconut shell.

#### Using an unfamiliar object as a container.

A researcher places a leftover coconut shell in front of Natura-1 after eating the coconut, using it as an unfamiliar container for a test. Natura-1 first picks up a small, smooth spoon, then uses it to scoop beans from a bowl. It must keep the spoon steady as it moves to avoid spilling, then position it over the shell’s narrow opening without hitting the rim. As it tilts the spoon to pour in the beans, Natura-1 must control its grip to keep the spoon from slipping. Finally, it places the spoon back beside the bowl.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v025-c11c3bc8/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Put the lemon in the bin.

#### Adapting to repeated interference as both the lemon and bin move.

This time, a researcher uses a long stick on three occasions to move the lemon and bin to different positions. Beyond the visual distraction from the stick, Natura-1 faces the harder task of locating both the moving lemon and bin and adjusting its movements as their positions change. In the experiment, it adjusts its movements on the fly based on their latest positions, allowing it to accurately grasp the moving lemon and place it in the bin.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v026-094fb206/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Follow the lemon as a person moves it in front of you, then grasp it.

#### Adjusting its reach as a person moves the lemon.

Asked to follow the lemon, Natura-1 tracks its movement in real time as a researcher moves it sideways, up and down, and toward or away from the robot. It uses continuous visual feedback to adjust both arms, keeping its hands aligned with the moving fruit rather than following a fixed, pre-planned path.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v035-e04aa195/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Pick up the tissue, pass it from one hand to the other three times, then place it on the book.

#### Passing a tissue between hands three times before placing it on a book.

Natura-1 faithfully executes a multi-step instruction with explicit sequential constraints. After pulling the tissue, the robot brings the sheet into the central workspace and carries out the three specified hand-to-hand transfers one after another, releasing with one hand only after the opposite fingers secure the delicate, shifting paper. Completing each transfer without dropping or tearing the tissue, Natura-1 neatly lays the tissue across the book cover, demonstrating precise instruction following throughout an extended bimanual process.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v037-5244d62c/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Stack the objects from largest to smallest by volume.

#### Stacking diverse objects from largest to smallest.

Natura-1 stacks objects of different shapes, sizes, and materials in descending order of volume, placing the largest at the base and progressively smaller objects above it. Beyond identifying the correct order, the robot must choose a suitable grasp and placement for each item, accounting for how it rests on the object below. The task brings together relative size comparison, instruction following, and dexterous manipulation to build a stable stack.

##### 01Nest the cups

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v021-73e0d17a/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Stack the three cups.

##### 02Add the orange

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v019-7801f548/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Place the orange on top of the cups.

##### 03Drape a tissue

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v020-ff7b9ca5/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Place a tissue over the orange.

#### Following successive requests to build an unusual arrangement.

Natura-1 follows three successive instructions without resetting the scene: stack three upside-down cups, place an orange on top, and cover it with a tissue. After stacking the cups, it places the orange on the top cup’s small base, controlling its position and release to keep the round fruit from rolling off or disturbing the stack. It then pulls a tissue from a tissue pack and attempts to lay it over the orange. This requires accurately grasping the soft, changing material and keeping the sheet spread out as it is lowered onto the curved orange.

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v022-06ee10c9/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

Instruction: Place the orange on the shirt, then fold the shirt.

#### Following an unusual request to fold a shirt around an orange.

Natura-1 takes an orange from a nearby basket, places it on a T-shirt, and folds the shirt around it with both hands. This is an unusual placement request. Even with the orange in view on the shirt, Natura-1 stays focused on the language instruction, folding the T-shirt around the orange. The shown clip ends with the shirt still on the table.

Strong instruction-following capabilities enable users to interact naturally with Natura-1, giving it the potential to become part of everyday life and turn the users' intentions into action. The video below presents a complete, nearly 30-minute recording of our everyday interactions with Natura-1, filmed in a single continuous take.

![Your browser does not support this video.](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/natura-1/local/posters/instruction-11s.jpg)Retry video ↻

### 3.4Emergent behaviors beyond predefined capabilities

This final section covers behaviors we did not set out to test. Dexterous control, instruction following, and long-horizon planning are the capabilities we deliberately built and measured. In daily interactions with Natura-1, however, we observe novel manipulation behaviors that our evaluations were not designed to capture. These behaviors emerge when the model encounters unfamiliar situations or difficulties during a task. Even without explicit guidance from robot demonstrations, it develops new approaches to continue working toward the goal.

When a grasp fails, a tool is unfamiliar, or the direct path is blocked, Natura-1 can find an alternative strategy: sliding a card over the edge of a yellow box to create a graspable overhang, using a rod to pull an object within reach, or turning its wrist mid-air to steady a toppling stack. None of these intermediate steps is specified in the prompt, and none appears in the robot demonstrations. The model devises them in response to the physical situation at hand.

We regard these behaviors as an early sign of more general physical intelligence. Learning from diverse human experience at scale appears to equip the model with an implicit understanding of physical mechanics, sufficient to invent solutions to unfamiliar problems rather than merely interpolate between previously seen trajectories.

**A bizarre setup, an improvised solution****A rod becomes a pointing tool****Another way to pick up a card****Pressing the spacebar on a laptop****Wrist rotation on retry****A pointing gesture, a different fold**

OBSERVATION 01 / 01

##### A bizarre setup, an improvised solution

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v034-79043c4d/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Grasp the rod0:01Draw the basket closer0:05Grasp the yarn0:07Lift out the yarn

##### Using the rod to pull an out-of-reach basket closer and retrieve the yarn.

Instruction: Try to grasp the yarn.

This scenario presents a deliberately bizarre arrangement: a basket containing yarn sits on an elevated platform beyond the robot's reach, with a long rod threaded through its handles. Retrieving an object far beyond arm's reach is no easy task, yet Natura-1 naturally devises a two-step plan. It grasps the near end of the rod, pulls it backward to haul the basket onto its workspace, and holds the rod steady with one hand while using the other to retrieve the yarn. By leveraging one object to bring another closer and dividing distinct roles between its two hands, the robot resolves an entirely unfamiliar setup through improvised physical reasoning.

OBSERVATION 01 / 01

##### A rod becomes a pointing tool

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v032-0cea8c41/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:01Grasp the rod0:04Tilt the rod upright0:08Touch the orange with the tip

##### Extending reach via an improvised pointing implement.

Instruction: Try to touch the orange.

Tasked with finding a way to touch an orange across from it, Natura-1 encounters a target placed on an elevated platform across from the robot—well beyond the physical reach of its arm and outside the standard tabletop setups of robot data collection. Recognizing that direct contact is impossible, the model devises its own solution: it turns to a long plastic rod lying on the table to bridge the distance. Natura-1 grasps the horizontal rod, tilts it upright, and steadily guides the distant tip onto the orange, maintaining continuous contact against the fruit. Controlling such an extended lever arm toward a target on an elevated plane requires significant spatial generalization. By autonomously adopting an unfamiliar tool to overcome a reach constraint, the model naturally treats the rod as an extension of its own arm.

OBSERVATION 01 / 02

##### The familiar pickup

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v031-dfe7e17a/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Reach for the card0:05Lift the card by its edge0:07Hold it with both hands

OBSERVATION 02 / 02

##### A new pickup

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v030-c28b682f/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Reach for the card0:04Slide past the box edge0:07Slip a hand underneath0:09Lift the card from below

COMPARE THE TWO PICKUP METHODS

01 / 02←→

![](https://media.naturewill.com/research-blog/media/v031-dfe7e17a/20261012T210313Z-089ca3c35ad7/cover.webp)0:09The familiar pickup![](https://media.naturewill.com/research-blog/media/v030-c28b682f/20261012T210313Z-089ca3c35ad7/cover.webp)0:09A new pickup

##### Creating a new grasp by using the box edge.

Instruction: Pick up the playing card.

Natura-1 was only taught to pick up a flat playing card by pinching its edge, as shown in the reference demonstration. In this trial, however, it adopts a different strategy from the outset: it slides the card horizontally across the box until part of it overhangs the rim, then slips its other hand into the newly created gap to lift the card from below. By using the edge of the box to create clearance for its fingers, the robot creates a new grasping opportunity rather than replaying a memorized grip.

OBSERVATION 01 / 01

##### Pressing the spacebar on a laptop

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v033-005124c2/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Aim the index finger0:02Press the spacebar0:03Lift the hand away

##### Translating broad pretrained knowledge into adaptive action.

Instruction: Press the spacebar.

Laptops and keyboards never appeared in Natura-1's robot training data, yet when instructed to "press the spacebar," the robot understands both the device and the action. It locates the spacebar among dozens of keys, presses it with its index finger until the screen lights up, and then lifts its hand away. This brief interaction shows how broad knowledge acquired during pretraining transfers directly into physical execution, producing the precise, single-finger coordination needed to operate an everyday human interface.

OBSERVATION 01 / 01

##### Wrist rotation on retry

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v027-4c69e838/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00The initial stack0:14The cups topple0:25Pick up the inverted cups0:35Rotate the wrist

##### Spontaneous wrist re-orientation under inverted grasp.

Instruction: Stack the three cups.

When an initial attempt to stack three cups causes two nested cups to topple onto the table, Natura-1 successfully picks them back up, but ends up holding the pair upside down. This leaves the robot in an unfamiliar corner case: the inverted opening cannot nest with the third cup through normal downward placement. Faced with this geometric conflict, Natura-1 spontaneously rotates its wrist nearly 180 degrees mid-air, attempting to turn the cups over and lower them onto the remaining cup. The wrist rotation itself is entirely emergent—faced with an awkward situation it was never trained on, the model invents a new spatial correction rather than mindlessly repeating its demonstrated routine.

OBSERVATION 01 / 02

##### The familiar routine

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v029-56c2e4af/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00The starting arrangement0:05Roll from the bottom

OBSERVATION 02 / 02

##### Recovery, then a new fold

![Your browser does not support this video.](https://media.naturewill.com/research-blog/media/v028-f48873bb/20261012T210313Z-089ca3c35ad7/cover.webp)Retry video ↻

0:00Try grasping the orange0:10Follow the gesture0:16Hand over the orange0:38Fold from the collar

COMPARE THE FOLDING TRIALS

01 / 02←→

![](https://media.naturewill.com/research-blog/media/v029-56c2e4af/20261012T210313Z-089ca3c35ad7/cover.webp)0:16The familiar routine![](https://media.naturewill.com/research-blog/media/v028-f48873bb/20261012T210313Z-089ca3c35ad7/cover.webp)0:58Recovery, then a new fold

##### Understanding a pointing gesture to retry, then folding in an undemonstrated direction.

Instruction (Reference trial): Fold the shirt and put it in the basket.

Instruction (Interrupted trial): Give the orange to the person, then fold the shirt.

Natura-1 was only taught to fold shirts by rolling them upward from the bottom, as shown in the reference demonstration. In the second trial, we introduce a new instruction: hand an orange to the researcher, then fold the shirt. During the hand-off, the orange accidentally drops onto the garment. Without any spoken command, the researcher simply points toward the fallen fruit; Natura-1 interprets this pointing gesture as a cue to target the indicated location and retry, re-grasps the orange, and deposits it into the person's open hand. Returning to the shirt, the robot does not revert to its familiar bottom-up routine, but instead begins folding from the collar downward. In doing so, it both grounds an unspoken human gesture in real time and discovers a reversed, undemonstrated trajectory to fold the garment.

4

## Built to Scale

Sustained dexterous workflows and zero-shot generalization do not happen by accident. They are the physical expressions of a learning system designed from the ground up to scale. Human experience is abundant but raw. Turning it into robot action takes three components: data that pairs each recording with language and action supervision, infrastructure that trains at scale and serves within a 100-millisecond control loop, and a model that learns the most from every trajectory. We design the three together, so that more experience translates into better action.

### 4.1Data

Physical intelligence requires learning from the breadth and structure of human experience. We build an end-to-end data system that continuously transforms human experience into training-ready video-language-action trajectories. The system integrates data acquisition, processing, annotation, distribution analysis, and large-scale infrastructure, enabling us to expand coverage while maintaining data quality as the dataset grows.

The foundation of this system is a large-scale and diverse human experience dataset. Our model is trained on **1 million hours of egocentric human data**, consisting of **61,702,471 episodes**, **317,842 tasks**, and **14,286 scenes**. The dataset is primarily built through controlled data acquisition, complemented by large-scale internet ego videos that further expand coverage. It includes monocular, stereo, and multi-camera recordings, as well as wrist-mounted views for fine-grained manipulation.

**Scaling Human Experience Collection.** Controlled data acquisition provides direct control over experience coverage. However, large-scale collection naturally favors simple and repeatable tasks, while complex activities requiring more preparation or specialized settings are often underrepresented.

We organize acquisition around a structured task taxonomy covering tasks, scenes, and interaction patterns. An agentic workflow backed by a database uses semantic retrieval to map data vendor proposals to our taxonomy, analyze existing coverage, and adjust acquisition priorities toward underrepresented areas. To further expand coverage beyond manually planned acquisition, we incorporate large-scale internet ego videos capturing naturally occurring human activities. These videos provide broader exposure to scenes, objects, and interaction patterns that are difficult to enumerate through controlled collection, further increasing the diversity of human experience represented in the dataset.

**Transforming Human Experience into Training Signals.** Raw first-person recordings contain rich behavioral information, but the information required for learning is often implicit. Our data pipeline transforms these observations into structured video-language-action trajectories through cleaning and annotation. Each processing operator is evaluated and refined using human-designed benchmarks to ensure reliable training signals.

**1. Cleaning.** We apply a unified cleaning pipeline across all data sources. We deduplicate the dataset using visual features, removing duplicate videos, overlapping segments, and highly similar clips across data vendors and internet sources. We also validate raw video and sensor data for completeness, readability, continuity, and temporal consistency. For internet ego videos, we further process the data to handle the variability of online content. Shot segmentation, hand visibility checks, model-based quality scoring, and VLM-based evaluation are combined to identify segments suitable for annotation and training.

**2. Motion Reconstruction.** Turning real-world first-person recordings into reliable motion labels is challenging. To address this challenge, we develop an in-house motion labeling pipeline for monocular and stereo ego videos. Through iterative improvements across data collection, training, and evaluation, the pipeline reconstructs dense hand and body motion from real-world recordings and transforms them into a unified representation. Our motion labels achieve a 41% reduction in MPJPE compared with existing open-source approaches on an internal benchmark with motion capture ground truth, providing reliable supervision for learning physical behaviors.

**3. Language Annotation.** Physical tasks are structured expressions of human intent, involving goals, intermediate steps, and interactions with the surrounding world. Capturing this structure requires supervision that goes beyond isolated action descriptions. Our annotation workflow uses an agentic architecture that shares context about each episode. The resulting annotations keep descriptions of task goals, intermediate steps, and individual actions consistent while capturing how interactions with objects and environments evolve over time.

**Measuring and Steering the Experience Distribution.** Large-scale datasets cannot be treated as static collections of examples. As the dataset grows, we need to understand what experience has been captured and how it aligns with training objectives.

Starting from semantic embeddings, we combine clustering algorithms and VLM-based semantic analysis to organize data into hierarchical structures, including task and scene trees. These structures reveal overrepresented and underrepresented regions of the experience distribution. With these insights, we continuously refine sampling strategies and data acquisition priorities, creating a feedback loop between dataset composition and model development.

**Scaling the Data System for Continuous Growth.** As the dataset grows, managing the full lifecycle of data—from acquisition and processing to training consumption—requires a unified infrastructure layer. Our data infrastructure provides scalable execution and reliable data management for the large-scale processing pipeline.

In the execution layer, we build a highly parallel pipeline based on Kubernetes. Elastic scheduling, automatic scaling, and failure recovery allow the system to adapt to changing workloads across different processing stages while maintaining reliable execution.

In the storage and management layer, we use Lakehouse to unify raw videos, sensor data, and intermediate processing artifacts. The platform currently manages **tens of PB** of data, providing a shared foundation for connecting processing stages and enabling efficient data selection for training.

The system processes **350,000 hours of ego data per week** and scales linearly with additional compute resources. This capability enables continuous iteration across data acquisition, processing, and model development, allowing the dataset to grow while maintaining quality, coverage, and operational efficiency.

### 4.2Infrastructure

Physical foundation models present two distinct computational demands: high-throughput training on large-scale multimodal trajectories, and real-time inference for physical robots within a strict **100-millisecond control-loop budget**. The former requires sustained efficiency across distributed compute; the latter requires precise control of latency throughout the execution path.

Standard distributed frameworks — built primarily for language modeling or offline batch inference — can introduce abstraction layers, memory overhead, and scheduling latency that are poorly suited to real-time physical interaction. Meeting both demands requires coordinated design across data pipelines, distributed execution, memory management, and GPU computation.

We built our training, inference, and GPU kernel frameworks in-house from scratch. On the inference side, we rewrote critical components in Rust—from the orchestrator control plane to the tensor runtime that executes the model—to reduce CPU overhead and keep GPUs saturated. On the training side, the stack is designed around the scale of our models and data. Across both, custom fused GPU kernels accelerate the most performance-critical operators. Sharing the same operator implementations across training and inference helps maintain numerical consistency and preserve model accuracy in deployment. Training and inference are designed together, so the path from large-scale learning to real-time control on physical robots is optimized end to end.

**Training.** Our training system combines a lightweight, modular architecture with the operational capabilities needed for sustained production runs. Clear interfaces between model recipes, data processing, optimization, and distributed execution let researchers introduce new architectures and learning objectives within an established training workflow.

This approach shortens the path from a working prototype to large-scale training. Research code retains the flexibility of native PyTorch while benefiting from established support for distributed execution, precision management, compilation, evaluation, and recovery. Infrastructure improvements carry forward into subsequent experiments as model scale and research complexity grow, without requiring researchers to repeatedly rebuild the training system.

For large-scale multimodal trajectories, we design data organization and compute scheduling together. Our purpose-built data pipeline sustains high-throughput training at scale, with an optimized data loader that avoids data-loading stalls even when reading from remote object storage. Distributed parallelism and memory optimizations extend these benefits to larger models and longer contexts. In our measured production configuration, **MFU exceeds 50% and GPU utilization reaches 98%**, turning more of the available compute into useful learning.

Our training infrastructure safeguards accumulated progress, allowing long-running experiments to resume reliably after interruptions. Integrated evaluation, monitoring, and profiling give researchers a clear view of model quality and system performance, helping them diagnose failures, identify bottlenecks, and improve subsequent runs.

**Inference.** Robot inference is a continuous process. Our inference framework serves multiple physical robots concurrently, with observations arriving asynchronously at any time. Each robot’s context must persist across requests, and every response must fit within its control budget. Our serving runtime therefore manages session state, resource ownership, and execution orchestration as core responsibilities.

A dedicated Rust control plane manages connections, request validation, preprocessing, and orchestration, while GPU workers execute coordinated inference steps. This separation allows request handling to progress independently of model computation, with each layer optimized for its own workload.

The runtime reduces repeated work through GPU-resident state, reusable caches, and captured execution graphs. Control messages and bulk payloads take separate paths, keeping orchestration lightweight and avoiding unnecessary data movement. Unified execution plans coordinate workers across GPUs, while completion reports keep session updates in step with completed computation. Device placement, communication, and cache management further reduce overhead along the critical path.

By optimizing the full serving workflow, we achieve **end-to-end inference latency within 100 milliseconds** and support responsive, continuous interaction between robots and their environments.

End-to-end observability makes latency optimization measurable. We track request handling, preprocessing, orchestration, and model execution separately to identify bottlenecks and determine whether a local improvement benefits the entire response path. Deployment constraints feed back into model and system design as we build increasingly capable models.

**Kernel.** A shared GPU kernel layer translates model computation into hardware-efficient execution across both training and real-time inference, enabling kernel optimizations and engineering insights to be reused across both environments. Designed to address their distinct computational demands, it targets recurring bottlenecks in attention, matrix operations, normalization, tensor transformations, and encoding, with implementations tailored to the shapes, layouts, and memory access patterns of real workloads.

We optimize arithmetic throughput, memory access efficiency, and GPU work organization. By fusing adjacent operations, reusing intermediate results, and dynamically adapting execution plans, we reduce redundant memory traffic and kernel-launch overhead. Savings on frequently executed paths accumulate across layers, execution steps, and training iterations, turning local optimizations into system-level gains.

Our custom attention kernels deliver approximately **1,200 TFLOP/s** on average across forward and backward benchmarks—**over 6× the throughput** of a tuned FlexAttention baseline. At the system level, our optimizations deliver **over 1.7× speedup** in end-to-end training and **2× speedup** in inference in the evaluated configurations.

Together, these layers give us direct control over the path from training data to robot response. As the infrastructure improves, research ideas reach large-scale experiments faster, compute budgets support more productive exploration, and models move into real-world deployment on a system that evolves alongside them.

### 4.3Model

Natura-1 is a single 50B mixture-of-experts transformer trained jointly on language, images, video, and action. Instruction understanding, world modeling, and action generation are handled by a single sequence model rather than separate subsystems, and three principles shape it: how much the model learns per unit of compute, how much it learns per trajectory, and what it learns about.

**Whole Trajectories on a Standard Transformer.** The first requirement of a foundation model is scalability: the architecture must never be the bottleneck, and every gain in training throughput should translate directly into learning. Natura-1 models an entire episode autoregressively as one sequence of language, image, video, and action tokens, so every forward and backward pass supervises every step of a trajectory, not a single sampled observation–action window. The backbone is a standard MoE transformer. Modality-specific inductive bias lives only in the sequence layout and the attention pattern, which keeps the core hardware-aligned and lets multimodal physical learning approach the training efficiency of frontier language and video models.

**Video and Action as One State.** At any moment, what the camera sees and what the hand does are two projections of the same physical state, so learning to predict video is also learning to act. This matters because video is the abundant modality: action labels are scarce and costly, while video dominates the tokens of every trajectory. Natura-1 uses past video as memory and learns to predict future video as part of its world model. It trains video and action together using flow matching and joint denoising, with a separate loss formulation for each modality. A trajectory yields far more supervision than its action labels alone — the basis for the robustness, memory, and recovery visible in the sustained workflows above.

**Prediction Is Not Understanding.** A model can fit the joint distribution of video and action and still ignore the instruction: in most clips the scene alone predicts what happens next, so language is the easiest signal to discard. Natura-1's pretraining makes language load-bearing. Using the fine-grained captions from our data pipeline, it is shaped so that a difference in stated intent yields a different predicted future, in video and action alike. In parallel, the model draws more fully on visual priors to read the scene an instruction refers to. Together, these approaches ground the zero-shot instruction following shown above in understanding rather than imitation.

---

The data, infrastructure and model above are built around a shared objective: turn more human experience into better action predictions. The scaling curves below show how Natura-1 progresses toward that objective. As training advances from approximately 44,000 to one million hours of experience, prediction error falls on both held-out human data and robot validation data.

On held-out human data, Action MSE decreases by **47.7%** and Action MAE by **37.3%**. Evaluating the same model weights on a held-out validation set of real-robot data shows improvements in robot action prediction as well: MSE decreases by **67.7%** and MAE by **49.3%** over the same training range, without further training for this evaluation. Both evaluations use teacher forcing, conditioning each prediction on the past observation.

These results support our integrated approach to scaling physical intelligence. With continued investment in data and compute, we aim to broaden the range of tasks and environments our models can handle, advancing toward a general-purpose physical foundation model.

5

## The Work Ahead

Natura-1 provides early evidence that generalization can coexist with the complexity of dexterous hands. Further progress depends on the full stack: more capable and stable effector and sensing systems, pretraining data at greater scale and coverage, and models that transfer to robots with less adaptation. We expect it to be a long-term research and engineering effort.

Citation

```
@misc{naturewill2026natura1,
title        = {{Natura-1: The Will to Act}},
author       = {{Nature Will Team}},
year         = {2026},
howpublished = {\url{https://www.naturewill.com/blog/natura-1}}
}
```

![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/36b4c.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/258f8.png)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/949c9.svg)

belief, updated by evidencethe measure of what is not yet knownthe proportion nature keepsleast action — will drives action![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/3670b.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/b31f7.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/3670b.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/b31f7.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/3670b.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/e9772.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/b31f7.svg)

physics shapes nature · will drives action

[![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/17982.svg)](https://x.com/naturewill)[![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/41cdc.svg)](https://www.youtube.com/channel/UC862ODFOVARM3ezMXHFDDfw)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/social-wechat.svg)![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/social-xiaohongshu.svg)[![](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/social-bilibili-wordmark.svg)](https://space.bilibili.com/3546858911697728)

@2026 Nature Will[京ICP备2026055952号-2](https://beian.miit.gov.cn/#/Integrated/index)

×

## WeChat Official Account

![QR code for Nature Will's WeChat official account](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/wechat-qr.jpg)

Scan with WeChat to follow Nature Will

## Xiaohongshu

![QR code for Nature Will's Xiaohongshu account](https://www.naturewill.com/_releases/b6d92871e3f8a0c84d9490786d7fa7d1e08c9ad9a452b981b187ade9422853ea/assets/xiaohongshu-qr.jpg)

Scan with Xiaohongshu

Close ×