#!/bin/bash

# Define parameters
NUM_RUNS=20                   # Number of repetitions for the test
OUTPUT_FILE="goodput_results_4a.csv"  # Output file to save the results
IPERF_SERVER="10.0.5.1"       # Server IP for iperf3 test

# Initialize output file
echo "Run Average_Goodput(Mbps) Std_Dev(Mbps)" > "$OUTPUT_FILE"

# Main loop for multiple runs
GOODPUTS=()
for ((i = 1; i <= NUM_RUNS; i++)); do
    echo "Run $i..."

    # Extract the receiver bitrate
    RESULT=$(iperf3 -c $IPERF_SERVER | grep "receiver" | awk '{print $(NF-2)}')

    # Verify extraction and store the value
    if [[ -n "$RESULT" ]]; then  # Check if RESULT is not empty
        GOODPUTS+=($RESULT)
        echo "Goodput for run $i: $RESULT Mbps"  # Optional debug output
    else
        echo "Error: No goodput value extracted for run $i"
    fi
done

# Calculate average and standard deviation
if [[ ${#GOODPUTS[@]} -gt 0 ]]; then  # Only calculate if GOODPUTS is not empty
    AVG=$(printf "%s\n" "${GOODPUTS[@]}" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
    STD_DEV=$(printf "%s\n" "${GOODPUTS[@]}" | awk -v avg="$AVG" '{sum+=($1-avg)^2} END {printf "%.2f", sqrt(sum/NR)}')
else
    AVG=0
    STD_DEV=0
fi

# Save results to file
echo "All ${NUM_RUNS} runs" >> "$OUTPUT_FILE"
echo "${AVG} ${STD_DEV}" >> "$OUTPUT_FILE"

echo "Experiment completed. Results saved to $OUTPUT_FILE"
