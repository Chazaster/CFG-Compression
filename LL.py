# Chase Watson, Adam May, Matt Mulkeen

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

    # Insert new element at the end of the LL; O(n) time
    def append(self, data):
        if not self.head:
            self.head = Node(data=data)
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(data=data, prev=current)

    # Insert new element at the beginning of LL; O(n) time
    def prepend(self, data):
        new_head = Node(data=data, next=self.head)
        if self.head:
            self.head.prev = new_head
        self.head = new_head

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