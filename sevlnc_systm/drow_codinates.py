import cv2
import numpy as np


cap = cv2.VideoCapture('walking.mp4')

# List to store points of the polygon
points = []

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

print('frame demention - ',height , width)


def draw_polygon(event, x, y, flags, param):
    global points

    # If left mouse button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the (x, y) coordinates to the points list
        points.append([x, y])

        # If there are at least two points, draw a line segment
        if len(points) > 1:
            cv2.line(image, points[-2], points[-1], (0, 255, 0), 2)

        cv2.imshow("Polygon Drawing", image)

    # If the user double clicks, close the polygon
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        if len(points) > 2:
            cv2.polylines(image, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)
            print("Polygon coordinates:", points)  # Print the polygon coordinates
            points.clear()  # Clear the list for the next polygon


# Create a black image to draw on
for x in range(50):
    r,img = cap.read()
    cv2.waitKey(1)

r,image = cap.read()

#image = np.zeros((512, 512, 3), dtype=np.uint8)

# Set up the mouse callback function
cv2.namedWindow("Polygon Drawing")
cv2.setMouseCallback("Polygon Drawing", draw_polygon)

while True:
    cv2.imshow("Polygon Drawing", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(points)

        polygon_coordinates = points

        # Create a blank image (black) as the background
        #width, height = 640, 480  # Adjust the size as needed

        mask = np.zeros((height, width), dtype=np.uint8)

        # Convert the polygon coordinates to a NumPy array
        polygon = np.array(polygon_coordinates, np.int32)

        # Reshape the polygon array to be in the shape (N, 1, 2), where N is the number of points
        polygon = polygon.reshape((-1, 1, 2))

        # Fill the polygon with white color (255) on the black background
        cv2.fillPoly(mask, [polygon], 255)

        # Save the binary mask as an .npy file
        np.save('abnomal_detect_restArea_MARKS.npy', mask)
        np.save('abnomal_detect_restArea_LINES.npy', points)

        cv2.polylines(mask, [np.array(points)], isClosed=True, color=(255), thickness=2)

        cv2.imshow('mask',mask)
        cv2.waitKey(0)




        break



#[[388, 286], [235, 286]]


cv2.destroyAllWindows()
