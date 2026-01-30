kola = good guy
moses = bad guy
business = neutral guy

def fight_scene():
    if kola + moses > 0:
        money = peace
    
    print ("Kola loves Moses")

    else if kola + moses <= 0:
    print("Kola confronts Moses in an epic showdown.")
    print("After a fierce battle, Kola emerges victorious, bringing peace to the land.")

def business_scene():
    if kola + business + moses > 0:
        print("Business thrives in the bustling market.")
    else:
        print("Business faces challenges but remains resilient.")



fight_scene()business_scene()


Sync functions = Learning on video call
Async functions = Learning via online course + self study + drawing a cow + reading my emails

Sync functions are like having a live video call with an instructor. You get real-time feedback, can ask questions immediately, and interact directly with the teacher and other students. This method is great for those who prefer structured learning environments and benefit from immediate clarification of doubts.

Async functions, on the other hand, are like taking an online course at your own pace.

Example:
Sync = run broker connection + run user registration + run payment processing + run user notification.

Async = run broker connection (while waiting for broker to connect after starting connection) + then run user registration + (while waiting for user registration) run payment processing + (while waiting for payment processing) run user notification.