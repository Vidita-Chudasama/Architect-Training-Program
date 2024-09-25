from collections import defaultdict

class ResourceAllocationGraph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list to represent the graph
    
    # Add an edge from a process to a resource or vice-versa
    def add_edge(self, u, v):
        self.graph[u].append(v)
    
    # DFS helper function to detect cycles
    def dfs(self, node, visited, rec_stack):
        # Mark the current node as visited
        visited[node] = True
        rec_stack[node] = True  # Add to recursion stack

        for neighbor in self.graph[node]:
            if not visited[neighbor]:
                if self.dfs(neighbor, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]:
                # If neighbor is in recursion stack, we found a cycle
                return True

        rec_stack[node] = False  # Remove the node from recursion stack
        return False
    
    def is_deadlock(self):
        visited = defaultdict(bool)
        rec_stack = defaultdict(bool)
        
        # Check for cycles in the graph
        for node in self.graph:
            if not visited[node]:
                if self.dfs(node, visited, rec_stack):
                    return True
        return False

def main():
    rag = ResourceAllocationGraph()
    
    # Processes: P0, P1, P2, P3, P4
    # Resources: R0, R1, R2
    
    rag.add_edge("P0", "R0")  # P0 holds R0
    rag.add_edge("P1", "R1")  # P1 holds R1
    rag.add_edge("R0", "P2")  # P2 is waiting for R0
    rag.add_edge("R1", "P3")  # P3 is waiting for R1
    rag.add_edge("P2", "R2")  # P2 holds R2
    rag.add_edge("R2", "P0")  # P0 is waiting for R2 (creates a cycle)

    if rag.is_deadlock():
        print("Deadlock detected!")
    else:
        print("No deadlock.")
    
if __name__ == "__main__":
    main()
