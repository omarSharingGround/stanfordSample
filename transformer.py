def bind_sentences(array1, array2):
    result = []

    # Convert time format from objects in array2
    def convert_time(entry):
        start_seconds = entry['start_time']['seconds'] + entry['start_time']['nanos'] * 1e-9
        end_seconds = entry['end_time']['seconds'] + entry['end_time']['nanos'] * 1e-9
        return start_seconds, end_seconds
    
    p1, p2 = 0, 0

    while p1 < len(array1):
        sentence1 = array1[p1]['text']
        begin_time1 = array1[p1]['start']
        end_time1 = begin_time1 + array1[p1]['duration']

        words_within_time_range = []

        while p2 < len(array2):
            word_start, word_end = convert_time(array2[p2])
            # If the current word's start time is past the end_time1, break the loop.
            if word_start > end_time1:
                break
            # Check if a word falls within the current sentence's time range.
            if begin_time1 <= word_start < end_time1 or begin_time1 < word_end <= end_time1 or word_start <= begin_time1 < word_end:
                words_within_time_range.append(array2[p2]['word'])
            p2 += 1

        sentence2 = ' '.join(words_within_time_range)

        result.append((sentence1, sentence2))
        
        p1 += 1

    return result

