from tkinter import *
import math
import winsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#FF8B8B"
RED = "#F15412"
GREEN = "#4E944F"
YELLOW = "#FFF9D7"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
checkmarks = ""
timer = None


# ---------------------------- TIMER RESET --------------------------------------- #
def reset_timer():
	window.after_cancel(timer)
	canvas.itemconfig(timer_text, text="00:00")
	timer_label.config(text="Timer", fg=GREEN)
	start_button.config(state="normal")
	global checkmarks
	checkmarks = ""
	checkmark_label.config(text=checkmarks)
	global reps
	reps = 0


# ---------------------------- TIMER MECHANISM ----------------------------------- #
def start_timer():
	global reps
	reps += 1

	work_sec = WORK_MIN * 60
	short_break_sec = SHORT_BREAK_MIN * 60
	long_break_sec = LONG_BREAK_MIN * 60

	beep_duration = 1000  # milliseconds
	beep_frequency = 1000  # Hz
	winsound.Beep(beep_frequency, beep_duration)  # emits 'beep' sound at the end of every work/break interval

	if reps % 8 == 0:
		# 8th rep
		count_down(long_break_sec)
		timer_label.config(text="Break", fg=RED)

	elif reps % 2 == 0:
		# 2nd/4th/6th rep
		count_down(short_break_sec)
		timer_label.config(text="Break", fg=PINK)

	else:
		# 1st/3rd/5th/7th rep
		count_down(work_sec)
		timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
	start_button.config(state="disabled")
	if count > 0:
		global timer
		timer = window.after(1000, count_down, count - 1)
	else:
		start_timer()
		if reps % 2 == 0:
			global checkmarks
			checkmarks += "✔"
		checkmark_label.config(text=checkmarks)

	count_min = math.floor(count / 60)
	count_sec = count % 60

	if count_sec < 10:
		count_sec = f"0{count_sec}"
	if count_min < 10:
		count_min = f"0{count_min}"

	canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")


# ---------------------------- UI SETUP ------------------------------------------ #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)


# Canvas
canvas = Canvas(width=202, height=226, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(101, 113, image=tomato_image)
timer_text = canvas.create_text(105, 130, text="00:00", fill="white", font=(FONT_NAME, 26, "bold"))
canvas.grid(column=1, row=1)


# Labels
timer_label = Label(text="Timer", font=(FONT_NAME, 36, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0)

checkmark_label = Label(font=(FONT_NAME, 14, "bold"), bg=YELLOW, fg=GREEN)
checkmark_label.grid(column=1, row=3)


# Buttons
start_button = Button(command=start_timer, text="Start", width=5, bg="white")
start_button.grid(column=0, row=2)

reset_button = Button(command=reset_timer, text="Reset", width=5, bg="white")
reset_button.grid(column=2, row=2)

window.mainloop()
