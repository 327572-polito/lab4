# Define parameters
LOSS_VALUES=$(seq 7 1 10)  # Packet loss values from 0% to 10% in steps of 0.5%
NUM_RUNS=20                   # Number of repetitions for each loss value
OUTPUT_FILE="goodput_results1b.csv"  # Output file to save the results
IPERF_SERVER="10.0.5.1"      # Server IP for iperf3 test
INTERFACE="eth0"             # Network interface for `tc` commands

# Initialize output file
echo "Loss(%) Average_Goodput(Mbps) Std_Dev(Mbps)" > "$OUTPUT_FILE"

# Main loop
for LOSS in $LOSS_VALUES; do
    echo "Testing with packet loss: $LOSS%"
    sudo tc qdisc change dev $INTERFACE root netem loss ${LOSS}%  # Set packet loss
    
    # Run iperf3 multiple times and collect goodput
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
    echo "${LOSS} ${AVG} ${STD_DEV}" >> "$OUTPUT_FILE"
done

# Reset the packet loss to 0% at the end
tc qdisc change dev $INTERFACE root netem loss 0%

echo "Experiment completed. Results saved to $OUTPUT_FILE"
