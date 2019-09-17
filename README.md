# Handwriting-Recognition

AI program to recognize handwriting. 
Currently prints out results in the console along with percentage of which letter it thought it was.

Current capabilities of this program include
- Currently using a simple one layer neural network to identify lowercase characters of the alphabet.
- Function to create feature arrays from image on canvas
- Letter window to collect data that is used for training the neural net
- User Window that allows user to write their own message and have it interpreted by the Neural Network
    - Allows user to write on canvas
    - Erase writing
    - Undo last drawing
    - Save state of window
- Uses OpenCV to recognize letters on canvas separately.
    - Added functionality to detect i's and j's correctly (dots and lines originally detected as two 
      separate objects)
    - Uses dilation to connect slightly disconnected letters (i.e. -> k with disconnected legs) 
- Added functionality to sort detected letters Left to Right, Top to bottom

Required Python3.0+ Libraries
1. Tkinter
2. numPy
3. opencv-python
4. pillow

# Future Work
- Add improved results printing for user (allow them to type sentences just by writing) -> close!
- Add more layers to the neural network.
- Implement my own Neural network/use popular library to achieve higher accuracy.
- Bring in more data (online) greater volume when training NN.

# References
 
 Most of neural net implementation written by Usman Malik, and obtained from
 https://stackabuse.com/creating-a-neural-network-from-scratch-in-python-multi-class-classification/

 - Thank you very much, this project was used for learning purposes.
