# QuestionExtractorAI (Work in progress)

The Question Extractor AI is a neural network trained to detect individual questions from exam images. A key constraint of this project is that it will not use Optical Character Recognition (OCR) or Natural Language Processing (NLP), as these methods are computationally expensive.

![readme_image1](/public/readme_image1.png)

## Why no OCR and NLP

The simplest way to extract exam questions would be to perform OCR and process the results with NLP. However, this approach seems like overkill, as the text density or layout alone should be sufficient to distinguish different questions.

As humans, we can detect individual questions from an exam even if it is written in an unfamiliar language. We can easily identify which figure belongs to which question, recognize that certain multiple-choice options correspond to the question above, distinguish exam headers from questions. We also understand that a gap in the text after multiple choices likely indicates the end of a question.

Therefore, I am working on training a neural network that can draw bounding boxes around each individual question based solely on text density, without relying on the actual text content.

![readme_image2](/public/readme_image2.png)


## Common Challenges 

![readme_image2](/public/readme_image3.png)

1. Different Page Layouts: Different exams have varying page layouts, including the spacing between lines, the gaps between questions, and the distance between questions and their choices. The position of the question number relative to the question itself can also vary. Handling these edge cases manually is extremely challenging and time-consuming.

2. Multiple-Choice Exams: In multiple-choice exams, the choices typically mark the end of the question. However, in exams without choices, like essay-style exams, how can we determine the start of the next question without resorting to computationally expensive OCR?

3. Nonlinear Layouts: Some exams, such as the SAT, do not follow a simple top-to-bottom layout but are divided into left and right halves. If we rely on traditional computer vision techniques, we would need to manually program the detection of these splits.

4. Distinguishing Headers and Footers: Exam headers and footers can be a nuisance. It would be ideal if our neural network could differentiate these from the actual exam content.

5. Spanning Questions Across Pages: Sometimes, questions span more than one page, with the question and its choices appearing on different pages. How can we connect these elements together effectively?


# DataSet

To generate a training set, we use OpenCV to annotate the exam files with computer vision techniques (same idea as this [Stack Overflow answer](https://stackoverflow.com/questions/71882225/slicing-of-a-scanned-image-based-on-large-white-spaces/71882633#71882633) ). As mentioned in the Common Challenges section above, this process can be tedious, as different exams require different parameters to make the openCV script work.

Navigate to the project directory in the terminal and run

```
python extract.py <file_location> [options]
```

I put some exam inside /tools/testing used for testing purpose, you can run
 `python extract.py ./tools/3/amc.jpg` and see the result in the ./tools/3/output folder. Required python3.12 (opencv,imutils,pdf2image)

**Arguments**

<file_location>: The path to the exam file (either an image or a PDF) that you want to process.

**Optional Flags**

*-type* : Specifies the type of exam layout to process. This flag accepts one of three values (1,2,3)

Example: `-type 1` (*Default:question number lead question content*), `-type 2` (*SAT*), `-type 3` (*question number does not lead question content*)

*-kernel* <width> <height>: Defines the width and height of the kernel used in dilation (refer to stackoverflow answer above). This is used to adjust the sensitivity of the bounding box detection.

Example: `-kernel 15 15`

*-top*: Crops out the top x% of the image or page. This is useful for removing headers or irrelevant content from the top of the page.

Example: `-top 10` (Crops out the top 10% of the page)

*-buttom*: Crops out the bottom x% of the image or page. This helps in excluding footers or unnecessary content from the bottom of the page.

Example: `-buttom 5` (Crops out the bottom 5% of the page)




# Model
Work in progress


# Result
Work in progress
