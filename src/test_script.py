def main():
    import datetime

    from prices import views


    views.running_programm()

    def run_the_parscin_script():
        get_year  = datetime.datetime.now().year
        get_month  = datetime.datetime.now().month
        get_day  = datetime.datetime.now().day

        start = datetime.datetime(get_year, get_month, get_day, 17, 8) # !!!!!!! для введения часа и мин ля запуска скрипта
        delta = datetime.timedelta(minutes=0)
        end = start + delta
        end_hour = end.hour
        end_minute = end.minute
        end_execution = start + datetime.timedelta(minutes=2)
        #print('end_hour', end_hour, 'end_minute', end_minute)
        couple_min_checking = datetime.timedelta(minutes=1)
        get_current_time = datetime.datetime.now()
        minutes_to_start_left =  start - get_current_time 
        #print('!!!', minutes_to_start_left)
        #if minutes_to_start_left < couple_min_checking: # если до времени запуска скрипта осталось менее минуты - то начать
            #while True:
            ##    print(datetime.datetime.now())
            #    current_time = datetime.datetime.now()
            #    if current_time.hour == end_hour and current_time.minute == end_minute:    
            #        belarus_sites_parsing()
            #        break
            #    elif current_time.hour == end_execution.hour and current_time.minute == end_execution.minute:  
            #        break


        if get_current_time > start:
            print(' +++++++++++ === =====++++++++the programm is FULLFILLED')
            views.running_programm()
        print('PROFECY IS FULLFILLED !!!!! OMENS IN THE SKY')
        #belarus_sites_parsing()
        #pass
        return 'the programm is fullfilled'



    run_the_parscin_script()


if __name__ == "__main__":
    main()



#import sys
#import os
#fpath = os.path.dirname(__file__)
#sys.path.append(fpath)
#print(fpath)
