# Chase Watson

class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        return repr(self.data)

# To remove from LL:
    # element = LL.find(42)
    # LL.removeElement(element)
class LinkedList:
    # This LL class will take O(1) time
    def __init__(self):
        self.head = None

    # Return a string representation of the LL; O(n) time
    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current))
            current = current.next
        return '[' + ', '.join(nodes) + ']'

    # Gets the length of the LL, similar to find; O(n) time
    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            if current and current.data != None:
                current = current.next
        return count

    # Insert new element at the end of the LL; O(n) time
    def append(self, data):
        # If LL is empty, populate LL with head of input
        if not self.head:
            self.head = Node(data=data)
            return
        # Set current to head of input
        current = self.head
        # Now get next's data
        while current.next:
            current = current.next
        current.next = Node(data=data, prev=current)

    # If data matches key, then return element. Else return None; O(n) time
    def find(self, key):
        current = self.head
        while current and current.data != key:
            current = current.next
        return current

    # Unlink an element from the LL; O(1) time
    def removeElement(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node is self.head:
            self.head = node.next
        node.prev = None
        node.next = None

    # Delete the first occurrence of key in the list; O(n) time
    def remove(self, key):
        element = self.find(key)
        if not element:
            return
        self.removeElement(element)

    # Get the head of the LL, used for traversals; O(1) time
    def start(self):
        return self.head

    # Get the next value directly after head; O(1) time
    def _next(self, key):
        return key.next