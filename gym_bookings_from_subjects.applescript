using terms from application "Mail"
    on perform mail action with messages theMessages for rule theRule
        set {year:y, month:m, day:d, time:t} to (current date)
        set subject_file to y & "_" & (m as number) & "_" & d & "_" & t & ".txt"
        set subject_file_path to "~/PycharmProjects/CatzGym/subject_files/" & subject_file
        do shell script "touch " & subject_file_path
        tell application "Mail"
            repeat with eachMessage in theMessages
                set this_subject to subject of eachMessage
                set this_sender to extract address from sender of eachMessage
                do shell script "echo \"" & this_subject & "\" >> " & subject_file_path
                do shell script "echo \"" & this_sender & "\" >> " & subject_file_path
            end repeat
        end tell
        do shell script "/usr/local/bin/python3 ~/PycharmProjects/CatzGym/parse_subjects.py " & subject_file
    end perform mail action with messages
end using terms from