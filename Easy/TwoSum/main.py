from manim import *
from collections import defaultdict

ANIMATE_CONFIG = {
    "run_time" : 0.15
}

class TwoSum(Scene):
    
    def __init__(self):
        super().__init__()
        self.TARGET = 24
        self.INPUT = [1, 4, 9, 13, 7, 4, 10,  11]

    def construct(self):
        self.water_ink()
        problemGroup = self.title_and_description(
            "Two Sum",
            {
                "font" : "Arial",
                "font_size" : 48
            },
            """
            Given an array of integers nums and an integer target, return indices of the two \n
            numbers such that they add up to target. You may assume that each input would have\n 
            exactly one solution, and you may not use the same element twice.\n
            You can return the answer in any order.
            """,
            {
                "font" : "Arial",
                "font_size" : 20,
                "t2c" : {
                    "nums" : BLUE, 
                    "target" : ORANGE
                }
            }
        )
        
        inputNumObjDict = {(idx, num) : Text(str(num)) for idx, num in enumerate(self.INPUT)}

        list_of_num = VGroup(
            [Text("[")] +
            list(inputNumObjDict.values()) +
            [Text("]")] 
        )\
            .arrange(buff=0.475).next_to(problemGroup, DOWN)\
            .shift(DOWN)\
            .align_to(problemGroup, LEFT)

        target_string = Text("target = ", font = "Arial", t2c = {"target" : ORANGE})\
            .next_to(list_of_num, RIGHT)\
            .align_to(problemGroup, RIGHT)
        
        target_text = Text(f"{self.TARGET}", font = "Arial")\
            .next_to(target_string, RIGHT)

        self.play(FadeIn(list_of_num, target_position = LEFT))
        self.play(FadeIn(VGroup([target_string, target_text]), target_position = RIGHT))
        
        self.wait(1)

        self.play(FadeOut(problemGroup))
        self.play(list_of_num.animate.to_corner(UL))
        self.play(VGroup([target_string, target_text]).animate.to_corner(UR))
        
        self.wait(1)
        # solution 1 - loop
        solution1Group = self.title_and_description(
            "Solution One: Double Loop",
            {
                 "font" : "Arial",
                 "font_size" : 20,
                 "t2c" : {
                    "nums" : BLUE, 
                    "target" : ORANGE
                 }
            },
            """
            The simplest approach is to use two nested loops with indices i and j , \n
            representing the first and second elements in the list. You check every possible pair, \n
            and if input[i] + input[j] == target, you've found the answer.\n
            This method is straightforward but not very efficient — it has a time complexity of O(n²).
            """,
            {
                 "font" : "Arial",
                 "font_size" : 20,
                 "t2c" : {
                    " i " : GREEN, 
                    " j " : RED 
                 }
            }
        )
        self.play(FadeOut(solution1Group))

        iArrows = [
            Arrow(start=list_of_num[i].get_bottom() + DOWN, end=list_of_num[i].get_bottom(), color = RED) for i in range(1, len(list_of_num) - 1)
        ]
        jArrows = [
            Arrow(start=list_of_num[j].get_bottom() + DOWN, end=list_of_num[j].get_bottom(), color = BLUE) for j in range(1, len(list_of_num) - 1)
        ]
        
        iArrow = iArrows[0]
        jArrow = jArrows[1]
        prevSum = Text(str(int(list_of_num[1].text) + int(list_of_num[2].text)))

        self.play(Create(iArrow))
        self.play(Create(jArrow))
        self.play(Create(prevSum))
        
        foundAnswer = False
        iAnsIdx = -1
        jAnsIdx = -1
        for i in range(len(iArrows)):    
            for j in range(i + 1, len(jArrows)):

                iArrow.target = iArrows[i]
                jArrow.target = jArrows[j]
                currentSumInt = int(list_of_num[i + 1].text) + int(list_of_num[j + 1].text)

                if currentSumInt == self.TARGET: 
                    foundAnswer = True
                    iAnsIdx = i
                    jAnsIdx = j
                    
                currentSum = Text(str(currentSumInt), color = RED if not foundAnswer else GREEN)
                
                self.play(MoveToTarget(iArrow, run_time=0.2))
                self.play(MoveToTarget(jArrow, run_time=0.2))
                self.play(Transform(prevSum, currentSum, run_time=0.2))
            
            if foundAnswer:
                break
        
        self.play(prevSum.animate.scale(1.25))
        self.play(prevSum.animate.scale(0.8))
        new_target_text = Text(f"{self.TARGET}", font = "Arial").move_to(target_text)
        self.play(Transform(target_text, new_target_text))
        self.wait(1)
        self.play(FadeOut(prevSum))

        list_of_index = VGroup(
            [
                Text(str(idx), color = GREEN).next_to(list_of_num[idx + 1], DOWN) if idx in [iAnsIdx, jAnsIdx] else Text(str(idx)).next_to(list_of_num[idx + 1], DOWN) for idx in range(len(list_of_num) - 2)
            ]
        ).next_to(list_of_num, DOWN).shift(DOWN).align_to(list_of_num[1], LEFT)
        
        self.play(Create(list_of_index))

        ansIndexText = VGroup([
            Text("Ans : ("),
            Text(str(iAnsIdx), color = GREEN),
            Text(","),
            Text(str(jAnsIdx), color = GREEN),
            Text(")")
        ]).arrange(buff = 0.475).next_to(list_of_index, DOWN).shift(DOWN)

        self.play(Create(ansIndexText))
        
        self.play(FadeOut(VGroup([list_of_index, ansIndexText, iArrow, jArrow])))
        
        # solution 2 - dictionary

        solution2Group = self.title_and_description(
            "Solution Two: Hash Table Lookup",
            {
                 "font" : "Arial",
                 "font_size" : 20,
                 "t2c" : {
                    "nums" : BLUE, 
                    "target" : ORANGE
                 }
            },
            """
            Another efficient approach is to use a hash table to keep track of the indices of\n 
            elements we've seen so far. As you iterate through the list, for each number, \n
            you check whether target - num already exists in the table. If it does, that means\n 
            you've found a pair that adds up to the target, and you can return the indices.\n
            If not, you store the current number and its index in the table for future reference.\n
            This method improves performance significantly, reducing the time complexity to O(n).\n
            """,
            {
                 "font" : "Arial",
                 "font_size" : 20,
                 "t2c" : {
                    "target" : ORANGE, 
                    "hash table" : RED 
                 }
            },
        )
        self.play(FadeOut(solution2Group))

        
        keySquaresDict = {}
        keySquaresList = []
        valueSquaresDict = {}
        valueSquaresList = []

        for idx, num in enumerate(self.INPUT): 
            keyObj = self.create_sqaure_text(num, WHITE)
            keySquaresDict[(idx, num)] = keyObj
            keySquaresList += [keyObj]

            valObj = self.create_sqaure_text("False", WHITE, 10)
            valueSquaresDict[num] = valObj
            valueSquaresList += [valObj]

        keySquaresGroup = VGroup(keySquaresList)\
            .arrange(direction=DOWN, buff = 0.05) \
            .next_to(list_of_num, DOWN)\
            .align_to(list_of_num, LEFT)\
            .shift(DOWN)

        valueSquaresGroup = VGroup(valueSquaresList) \
            .arrange(direction=DOWN, buff = 0.05) \
            .next_to(keySquaresGroup, RIGHT) \
            .shift(RIGHT)
        
        kvLinesList = []
        for (keyObj, valObj) in zip(keySquaresList, valueSquaresList):
            kvLinesList += [Arrow(start = keyObj.get_right(), end = valObj.get_left())]
        kvLinesGroup = VGroup(kvLinesList)
        
        dotsGroup = VGroup([Dot(radius=0.05), Dot(radius=0.05), Dot(radius=0.05)]) \
            .arrange(direction=DOWN, buff = 0.2) \
            .next_to(kvLinesGroup, DOWN)

        indexText = Text("(Index)", font = "Arial", font_size = 16).next_to(valueSquaresGroup, UP)
        valueText = Text("(Value)", font = "Arial", font_size = 16).next_to(keySquaresGroup, UP)

        kvMapGroup = VGroup(indexText, valueText, keySquaresGroup, kvLinesGroup, valueSquaresGroup, dotsGroup)
        self.play(Create(kvMapGroup))
        
        self.wait(1)

        minuendObj = Text(f"{self.TARGET}", font="Arial", color = ORANGE) \
            .next_to(target_text, ORIGIN)
        
        self.play(Create(minuendObj))

        self.play( 
            minuendObj.animate.scale(0.5).next_to(kvMapGroup, RIGHT * 4)
            )

        minusObj = Text(" - ").next_to(minuendObj, RIGHT)

        self.play(Create(minusObj))
            
        iArrows = [Arrow(start=list_of_num[i].get_bottom() + DOWN, end=list_of_num[i].get_bottom(), color = WHITE) for i in range(1, len(list_of_num) - 1)]
        table = defaultdict(bool)
        indexArrow = iArrows[0]
        subtrahendObj = Text("")
        differenceObj = Text("")
        
        for idx, num in enumerate(self.INPUT):

            # move arrow
            self.play(list_of_num[1 + idx].animate.set_color(GREEN), **ANIMATE_CONFIG)
            indexArrow.target = iArrows[idx]
            self.play(MoveToTarget(indexArrow, **ANIMATE_CONFIG))

            # update equation
            difference = self.TARGET - num
            new_subtrahendObj = Text(str(num) + " = ", color=GREEN, t2c={"=" : WHITE}, font_size = minuendObj.get_font_size()).next_to(minusObj, RIGHT)
            new_differenceObj = Text(f"{difference}", color = WHITE, font_size = minuendObj.get_font_size()).next_to(new_subtrahendObj, RIGHT)
            self.play(
                Transform(subtrahendObj, new_subtrahendObj), 
                keySquaresDict[(idx, num)].animate.set_color(GREEN),
                Transform(differenceObj, new_differenceObj),
                **ANIMATE_CONFIG
            )

            if table[self.TARGET - num] != False:

                valObj = valueSquaresList[idx]
                newValObj = self.create_sqaure_text(idx, GREEN, 10).move_to(valObj)
                valueSquaresDict[idx] = newValObj
                valueSquaresList[idx] = newValObj
                self.play(FadeOut(valObj), Write(newValObj), **ANIMATE_CONFIG)
                
                # update difference to green
                self.play(differenceObj.animate.set_color(GREEN).scale(1.25), **ANIMATE_CONFIG)
                # find answer
                answerKeyObj = None
                answerValObj = None
                for i, v in enumerate(self.INPUT): # find pair obj
                    if v == difference:
                        answerKeyObj = keySquaresList[i]
                        answerValObj = valueSquaresList[i]
                if answerKeyObj and answerValObj:
                    self.play(answerKeyObj.animate.set_color(GREEN).scale(1.25), answerValObj.animate.set_color(GREEN).scale(1.25))
                    self.play(answerKeyObj.animate.scale(0.8), answerValObj.animate.scale(0.8), differenceObj.animate.scale(0.8))

                ansIndexText = VGroup([
                    Text("Ans : ("),
                    Text(answerValObj[1].text, color = GREEN),
                    Text(","),
                    Text(newValObj[1].text, color = GREEN),
                    Text(")")
                ]).arrange(buff = 0.475).next_to(differenceObj, RIGHT).shift(RIGHT)

                self.play(Write(ansIndexText))

            else:
                # update difference to red 
                self.play(differenceObj.animate.set_color(RED), **ANIMATE_CONFIG)
                # update table
                valObj = valueSquaresList[idx]
                newValObj = self.create_sqaure_text(idx, WHITE, 16).move_to(valObj)
                valueSquaresDict[idx] = newValObj
                valueSquaresList[idx] = newValObj
                table[num] = idx + 1
                
                self.play(FadeOut(valObj), Write(newValObj), **ANIMATE_CONFIG)

            self.play(list_of_num[1 + idx].animate.set_color(WHITE), keySquaresDict[(idx, num)].animate.set_color(WHITE))



        self.wait(1)


        
    def title_and_description(self, title = "", title_config = {}, description = "", description_config = {}):

        solution1Description = Text(
            description,
            **description_config
        )
        
        solution1Title = Text(title,
            **title_config
        ).align_to(solution1Description, LEFT)

        solution1Group = VGroup(solution1Title, solution1Description).arrange(DOWN, buff=1)

        self.play(Write(solution1Title), FadeIn(solution1Description))
        self.wait(3)

        return solution1Group

        

    def create_sqaure_text(self, txt, color, size = 16):

        group = VGroup()
        
        square = Square(side_length=.5, color=color)

        text = Text(str(txt), font_size=size).move_to(square.get_center())

        group.add(square, text)

        return group
    
    def water_ink(self):
        
        # Create the text object
        floating_text = Text("github nonStopChou LeetcodeAnimation", font_size = 20, fill_opacity=0.3)
        floating_text.move_to(ORIGIN)

        # Initial velocity
        velocity = np.array([1.2, 0.8, 0])  # x, y, z direction

        # Set screen boundaries (based on default frame size)
        x_limit = config.frame_width / 2 - floating_text.width / 2
        y_limit = config.frame_height / 2 - floating_text.height / 2

        # Add updater for bouncing effect
        def bounce_updater(mob, dt):
            nonlocal velocity

            # Compute new position
            pos = mob.get_center() + velocity * dt

            # Bounce off walls by inverting velocity direction
            if abs(pos[0]) >= x_limit:
                velocity[0] *= -1
                mob.set_color(random_bright_color())

            if abs(pos[1]) >= y_limit:
                velocity[1] *= -1
                mob.set_color(random_bright_color())

            mob.move_to(mob.get_center() + velocity * dt)

        floating_text.add_updater(bounce_updater)
        self.add(floating_text)