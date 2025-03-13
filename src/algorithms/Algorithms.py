import sys
from ..sim_objects.Median import Median

def find_new_head(head: Median):
    """
        Sets the new head to be the median that is closest to the origin.
    """
    j = 0
    new_head = 0
    closest_to_origin = sys.maxsize
    median = head
    while median.next:
        distance_to_origin = median.distance_to_origin()
        # Early stopping
        if distance_to_origin > closest_to_origin:
            break

        if distance_to_origin < closest_to_origin:
            closest_to_origin = distance_to_origin
            new_head = j
        median = median.next
        j += 1
    
    median = head
    for i in range(new_head):
        median = median.next

    return median