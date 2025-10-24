import heapq
from typing import Dict, List, Tuple, Optional, Any

class StudentRegistry:
    """
    Manages student records using a fast lookup dictionary.
    
    This module handles all student information with quick access times.
    We use a dictionary as our main storage since it provides instant access
    to student records by their ID.
    """
    
    def __init__(self):
        # Stores students by their ID for quick access
        self.students = {}
        
    def register_student(self, student_id: str, name: str, course_id: str) -> bool:
        """Add a new student to the system."""
        if student_id in self.students:
            print(f"Error: Student ID {student_id} already exists!")
            return False
        self.students[student_id] = {
            'name': name,
            'course_id': course_id
        }
        print(f"Student {name} (ID: {student_id}) registered successfully!")
        return True
        
    def search_student(self, student_id: str) -> Optional[Dict]:
        """Find a student by their ID."""
        if student_id in self.students:
            return self.students[student_id]
        print("Record Not Found.")
        return None
        
    def update_student_info(self, student_id: str, new_data: Dict) -> bool:
        """Update information for an existing student."""
        if student_id not in self.students:
            print("Student not found!")
            return False
        self.students[student_id].update(new_data)
        print(f"Student {student_id} updated successfully!")
        return True
        
    def delete_student(self, student_id: str) -> bool:
        """Remove a student from the system."""
        if student_id not in self.students:
            print("Student not found!")
            return False
        del self.students[student_id]
        print(f"Student {student_id} deleted successfully!")
        return True
        
    def display_all_students(self):
        """Show all registered students."""
        if not self.students:
            print("No students registered.")
            return
            
        print("\n=== ALL STUDENTS ===")
        for student_id, info in self.students.items():
            print(f"ID: {student_id}, Name: {info['name']}, Course: {info['course_id']}")


class CourseScheduler:
    """
    Handles course registrations using a first-come, first-served queue.
    
    Students are processed in the order they register, just like waiting in line.
    Each course has limited spots, so we process requests until courses fill up.
    """
    
    def __init__(self):
        # Students wait in line for course registration
        self.registration_queue = []
        # Tracks which students got into which courses
        self.course_allocations = {}
        # How many students each course can hold
        self.course_capacity = {'CS101': 2, 'MATH201': 2, 'PHY301': 1}
        
    def enrol_student_request(self, student_id: str, course_id: str):
        """Add a student to the waiting list for a course."""
        self.registration_queue.append((student_id, course_id))
        print(f"Registration request queued: Student {student_id} for {course_id}")
        
    def process_queue(self):
        """Process all waiting registration requests."""
        if not self.registration_queue:
            print("No pending registration requests.")
            return
            
        print("\n=== PROCESSING REGISTRATION QUEUE ===")
        while self.registration_queue:
            student_id, course_id = self.registration_queue.pop(0)  # Take next in line
            
            if course_id not in self.course_capacity:
                print(f"Course {course_id} not found for student {student_id}")
                continue
                
            # Set up tracking for new courses
            if course_id not in self.course_allocations:
                self.course_allocations[course_id] = []
                
            # Check if there's still room in the course
            if len(self.course_allocations[course_id]) < self.course_capacity[course_id]:
                self.course_allocations[course_id].append(student_id)
                print(f"✓ Student {student_id} enrolled in {course_id}")
            else:
                print(f"✗ Course Full: {course_id} for student {student_id}")
                
    def display_course_allocations(self):
        """Show which students are enrolled in each course."""
        if not self.course_allocations:
            print("No course allocations yet.")
            return
            
        print("\n=== COURSE ALLOCATIONS ===")
        for course_id, students in self.course_allocations.items():
            print(f"{course_id}: {students}")


class PaymentNode:
    """Represents a single student's payment information in our tracking tree."""
    
    def __init__(self, student_id: str, amount_paid: float, total_fee: float):
        self.student_id = student_id
        self.amount_paid = amount_paid
        self.total_fee = total_fee
        self.balance = total_fee - amount_paid
        self.left = None
        self.right = None


class FeeTracking:
    """
    Tracks student payments using a binary search tree for efficient lookups.
    
    The tree keeps payment records sorted by student ID, making it easy to find
    any student's payment status and generate sorted reports.
    """
    
    def __init__(self):
        self.root = None
        
    def add_payment_record(self, student_id: str, amount_paid: float, total_fee: float) -> bool:
        """Add a new payment record to our tracking system."""
        new_node = PaymentNode(student_id, amount_paid, total_fee)
        
        if self.root is None:
            self.root = new_node
            print(f"Payment record added for student {student_id}")
            return True
            
        # Find the right spot in the tree for this student
        current = self.root
        while current:
            if student_id < current.student_id:
                if current.left is None:
                    current.left = new_node
                    print(f"Payment record added for student {student_id}")
                    return True
                current = current.left
            elif student_id > current.student_id:
                if current.right is None:
                    current.right = new_node
                    print(f"Payment record added for student {student_id}")
                    return True
                current = current.right
            else:
                print(f"Payment record for student {student_id} already exists!")
                return False
                
    def _search_node(self, student_id: str) -> Optional[PaymentNode]:
        """Find a student's payment record in the tree."""
        current = self.root
        while current:
            if student_id == current.student_id:
                return current
            elif student_id < current.student_id:
                current = current.left
            else:
                current = current.right
        return None
        
    def search_payment_record(self, student_id: str) -> Optional[Dict]:
        """Look up a student's payment details."""
        node = self._search_node(student_id)
        if node:
            status = "Cleared" if node.balance <= 0 else "Pending"
            record = {
                'student_id': node.student_id,
                'amount_paid': node.amount_paid,
                'total_fee': node.total_fee,
                'balance': node.balance,
                'status': status
            }
            print(f"Payment Record: {record}")
            return record
        else:
            print("Payment record not found!")
            return None
            
    def update_payment_record(self, student_id: str, new_amount: float) -> bool:
        """Update how much a student has paid."""
        node = self._search_node(student_id)
        if node:
            node.amount_paid = new_amount
            node.balance = node.total_fee - new_amount
            print(f"Payment record updated for student {student_id}")
            return True
        else:
            print("Payment record not found!")
            return False
            
    def _inorder_traversal(self, node: PaymentNode, result: List):
        """Collect all payment records in sorted order."""
        if node:
            self._inorder_traversal(node.left, result)
            status = "Cleared" if node.balance <= 0 else "Pending"
            result.append({
                'student_id': node.student_id,
                'amount_paid': node.amount_paid,
                'total_fee': node.total_fee,
                'balance': node.balance,
                'status': status
            })
            self._inorder_traversal(node.right, result)
            
    def generate_fee_clearance_report(self):
        """Create a sorted list of all students' payment statuses."""
        if self.root is None:
            print("No payment records available.")
            return
            
        result = []
        self._inorder_traversal(self.root, result)
        
        print("\n=== FEE CLEARANCE REPORT ===")
        for record in result:
            print(f"ID: {record['student_id']}, Paid: ${record['amount_paid']}, "
                  f"Total: ${record['total_fee']}, Balance: ${record['balance']}, "
                  f"Status: {record['status']}")


class LibrarySystem:
    """
    Manages book borrowing and returns using quick-access storage.
    
    We use a dictionary to instantly find books by their ISBN number,
    making checkouts and returns fast and efficient.
    """
    
    def __init__(self):
        self.books = {}
        
    def add_book(self, isbn: str, title: str, copies: int):
        """Add a new book to the library collection."""
        self.books[isbn] = {
            'title': title,
            'total_copies': copies,
            'available_copies': copies,
            'borrowers': []
        }
        print(f"Book '{title}' (ISBN: {isbn}) added with {copies} copies.")
        
    def borrow_book(self, isbn: str, student_id: str) -> bool:
        """Check out a book to a student."""
        if isbn not in self.books:
            print("Book Not Found!")
            return False
            
        book = self.books[isbn]
        if book['available_copies'] <= 0:
            print("Book Unavailable!")
            return False
            
        book['available_copies'] -= 1
        book['borrowers'].append(student_id)
        print(f"Student {student_id} borrowed '{book['title']}'")
        return True
        
    def return_book(self, isbn: str, student_id: str) -> bool:
        """Return a borrowed book to the library."""
        if isbn not in self.books:
            print("Book Not Found!")
            return False
            
        book = self.books[isbn]
        if student_id in book['borrowers']:
            book['available_copies'] += 1
            book['borrowers'].remove(student_id)
            print(f"Student {student_id} returned '{book['title']}'")
            return True
        else:
            print(f"Student {student_id} didn't borrow this book!")
            return False
            
    def check_availability(self, isbn: str):
        """Check how many copies of a book are available."""
        if isbn not in self.books:
            print("Book Not Found!")
            return
            
        book = self.books[isbn]
        print(f"Book '{book['title']}': {book['available_copies']} copies available "
              f"out of {book['total_copies']} total.")


class PerformanceAnalytics:
    """
    Analyzes student performance using a max-heap to quickly find top performers.
    
    The heap keeps the highest-scoring students readily accessible at the top,
    making it easy to identify and reward academic excellence.
    """
    
    def __init__(self):
        # We store negative scores to simulate a max-heap using Python's min-heap
        self.heap = []
        self.student_scores = {}
        
    def add_performance_record(self, student_id: str, scores_list: List[float]):
        """Add a student's performance data to our analytics."""
        average_score = sum(scores_list) / len(scores_list)
        
        # Store in heap (using negative for max heap with heapq)
        heapq.heappush(self.heap, (-average_score, student_id))
        
        # Keep detailed records for reporting
        self.student_scores[student_id] = {
            'scores': scores_list,
            'average': average_score
        }
        print(f"Performance record added for student {student_id} with average {average_score:.2f}")
        
    def display_top_performer(self, k: int = 1):
        """Show the top performing students."""
        if not self.heap:
            print("No performance records available.")
            return
            
        print(f"\n=== TOP {k} PERFORMER(S) ===")
        # Work with a copy to avoid modifying our main heap
        temp_heap = self.heap.copy()
        
        for i in range(min(k, len(temp_heap))):
            if not temp_heap:
                break
            neg_avg, student_id = heapq.heappop(temp_heap)
            avg_score = -neg_avg
            details = self.student_scores[student_id]
            print(f"{i+1}. Student {student_id}: Average = {avg_score:.2f}, "
                  f"Scores = {details['scores']}")
                  
    def view_all_rankings(self):
        """Show all students ranked from highest to lowest performance."""
        if not self.heap:
            print("No performance records available.")
            return
            
        print("\n=== ALL RANKINGS (Highest to Lowest) ===")
        # Sort all records by performance
        sorted_records = []
        temp_heap = self.heap.copy()
        
        while temp_heap:
            neg_avg, student_id = heapq.heappop(temp_heap)
            avg_score = -neg_avg
            sorted_records.append((student_id, avg_score))
            
        for i, (student_id, avg_score) in enumerate(sorted_records):
            details = self.student_scores[student_id]
            print(f"{i+1}. Student {student_id}: Average = {avg_score:.2f}, "
                  f"Scores = {details['scores']}")


class SchoolManager:
    """
    The main coordinator that brings all school management modules together.
    
    This class serves as the central hub, connecting all the different parts
    of our school system and providing a unified interface for users.
    """
    
    def __init__(self):
        self.student_registry = StudentRegistry()
        self.course_scheduler = CourseScheduler()
        self.fee_tracking = FeeTracking()
        self.library_system = LibrarySystem()
        self.performance_analytics = PerformanceAnalytics()
        
    def display_menu(self):
        """Show the main navigation menu."""
        print("\n" + "="*50)
        print("      SCHOOL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Student Registry")
        print("2. Course Scheduling") 
        print("3. Fee Tracking")
        print("4. Library System")
        print("5. Performance Analytics")
        print("6. Run Demo Sequence")
        print("7. Exit")
        print("="*50)
        
    def student_registry_menu(self):
        """Handle all student record operations."""
        while True:
            print("\n--- STUDENT REGISTRY ---")
            print("1. Register Student")
            print("2. Search Student")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Display All Students")
            print("6. Back to Main Menu")
            
            choice = input("Enter choice (1-6): ")
            
            if choice == '1':
                id = input("Enter Student ID: ")
                name = input("Enter Student Name: ")
                course = input("Enter Course ID: ")
                self.student_registry.register_student(id, name, course)
                
            elif choice == '2':
                id = input("Enter Student ID to search: ")
                result = self.student_registry.search_student(id)
                if result:
                    print(f"Found: {result}")
                    
            elif choice == '3':
                id = input("Enter Student ID to update: ")
                name = input("Enter new name: ")
                course = input("Enter new course: ")
                self.student_registry.update_student_info(id, {'name': name, 'course_id': course})
                
            elif choice == '4':
                id = input("Enter Student ID to delete: ")
                self.student_registry.delete_student(id)
                
            elif choice == '5':
                self.student_registry.display_all_students()
                
            elif choice == '6':
                break
            else:
                print("Invalid choice!")
                
    def course_scheduling_menu(self):
        """Manage course registration and assignments."""
        while True:
            print("\n--- COURSE SCHEDULING ---")
            print("1. Enrol Student Request")
            print("2. Process Registration Queue")
            print("3. Display Course Allocations")
            print("4. Back to Main Menu")
            
            choice = input("Enter choice (1-4): ")
            
            if choice == '1':
                student_id = input("Enter Student ID: ")
                course_id = input("Enter Course ID: ")
                self.course_scheduler.enrol_student_request(student_id, course_id)
                
            elif choice == '2':
                self.course_scheduler.process_queue()
                
            elif choice == '3':
                self.course_scheduler.display_course_allocations()
                
            elif choice == '4':
                break
            else:
                print("Invalid choice!")
                
    def fee_tracking_menu(self):
        """Handle student payment records and fee status."""
        while True:
            print("\n--- FEE TRACKING ---")
            print("1. Add Payment Record")
            print("2. Search Payment Record")
            print("3. Update Payment Record")
            print("4. Generate Fee Clearance Report")
            print("5. Back to Main Menu")
            
            choice = input("Enter choice (1-5): ")
            
            if choice == '1':
                student_id = input("Enter Student ID: ")
                amount = float(input("Enter Amount Paid: "))
                total = float(input("Enter Total Fee: "))
                self.fee_tracking.add_payment_record(student_id, amount, total)
                
            elif choice == '2':
                student_id = input("Enter Student ID to search: ")
                self.fee_tracking.search_payment_record(student_id)
                
            elif choice == '3':
                student_id = input("Enter Student ID to update: ")
                new_amount = float(input("Enter new amount paid: "))
                self.fee_tracking.update_payment_record(student_id, new_amount)
                
            elif choice == '4':
                self.fee_tracking.generate_fee_clearance_report()
                
            elif choice == '5':
                break
            else:
                print("Invalid choice!")
                
    def library_system_menu(self):
        """Manage book inventory and borrowing operations."""
        while True:
            print("\n--- LIBRARY SYSTEM ---")
            print("1. Add Book")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. Check Availability")
            print("5. Back to Main Menu")
            
            choice = input("Enter choice (1-5): ")
            
            if choice == '1':
                isbn = input("Enter ISBN: ")
                title = input("Enter Book Title: ")
                copies = int(input("Enter Number of Copies: "))
                self.library_system.add_book(isbn, title, copies)
                
            elif choice == '2':
                isbn = input("Enter ISBN: ")
                student_id = input("Enter Student ID: ")
                self.library_system.borrow_book(isbn, student_id)
                
            elif choice == '3':
                isbn = input("Enter ISBN: ")
                student_id = input("Enter Student ID: ")
                self.library_system.return_book(isbn, student_id)
                
            elif choice == '4':
                isbn = input("Enter ISBN: ")
                self.library_system.check_availability(isbn)
                
            elif choice == '5':
                break
            else:
                print("Invalid choice!")
                
    def performance_analytics_menu(self):
        """Analyze and display student performance data."""
        while True:
            print("\n--- PERFORMANCE ANALYTICS ---")
            print("1. Add Performance Record")
            print("2. Display Top Performer")
            print("3. View All Rankings")
            print("4. Back to Main Menu")
            
            choice = input("Enter choice (1-4): ")
            
            if choice == '1':
                student_id = input("Enter Student ID: ")
                scores = input("Enter scores (comma-separated): ")
                scores_list = [float(x.strip()) for x in scores.split(',')]
                self.performance_analytics.add_performance_record(student_id, scores_list)
                
            elif choice == '2':
                k = input("Enter number of top performers (default 1): ")
                k = int(k) if k.isdigit() else 1
                self.performance_analytics.display_top_performer(k)
                
            elif choice == '3':
                self.performance_analytics.view_all_rankings()
                
            elif choice == '4':
                break
            else:
                print("Invalid choice!")
                
    def run_demo_sequence(self):
        """Run a complete demonstration showing all system capabilities."""
        print("\n" + "="*60)
        print("          DEMONSTRATING ALL MODULES")
        print("="*60)
        
        # Show how student registration works
        print("\n1. MANAGING STUDENT RECORDS")
        print("-" * 50)
        self.student_registry.register_student("S001", "Alice Johnson", "CS101")
        self.student_registry.register_student("S002", "Bob Smith", "MATH201")
        self.student_registry.register_student("S003", "Carol Davis", "PHY301")
        self.student_registry.display_all_students()
        
        # Demonstrate quick student lookup
        print("\nFinding student S002:")
        result = self.student_registry.search_student("S002")
        
        # Show course registration process
        print("\n2. HANDLING COURSE REGISTRATIONS")
        print("-" * 50)
        self.course_scheduler.enrol_student_request("S001", "CS101")
        self.course_scheduler.enrol_student_request("S002", "CS101")
        self.course_scheduler.enrol_student_request("S003", "CS101")  # This one won't fit
        self.course_scheduler.enrol_student_request("S001", "MATH201")
        self.course_scheduler.process_queue()
        self.course_scheduler.display_course_allocations()
        
        # Demonstrate payment tracking
        print("\n3. TRACKING FEE PAYMENTS")
        print("-" * 50)
        self.fee_tracking.add_payment_record("S001", 500, 1000)
        self.fee_tracking.add_payment_record("S002", 1200, 1200)
        self.fee_tracking.add_payment_record("S003", 300, 1500)
        self.fee_tracking.search_payment_record("S002")
        self.fee_tracking.generate_fee_clearance_report()
        
        # Show library operations
        print("\n4. MANAGING LIBRARY BOOKS")
        print("-" * 50)
        self.library_system.add_book("ISBN001", "Introduction to Python", 2)
        self.library_system.add_book("ISBN002", "Advanced Algorithms", 1)
        self.library_system.borrow_book("ISBN001", "S001")
        self.library_system.borrow_book("ISBN001", "S002")
        self.library_system.borrow_book("ISBN001", "S003")  # Should be unavailable
        self.library_system.check_availability("ISBN001")
        
        # Demonstrate performance analysis
        print("\n5. ANALYZING STUDENT PERFORMANCE")
        print("-" * 50)
        self.performance_analytics.add_performance_record("S001", [85, 90, 78, 92])
        self.performance_analytics.add_performance_record("S002", [95, 88, 92, 96])
        self.performance_analytics.add_performance_record("S003", [75, 82, 79, 88])
        self.performance_analytics.display_top_performer()
        self.performance_analytics.view_all_rankings()
        
        print("\n" + "="*60)
        print("          DEMONSTRATION COMPLETED")
        print("="*60)
        
    def run(self):
        """Start the main application loop."""
        print("Welcome to School Management System!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                self.student_registry_menu()
            elif choice == '2':
                self.course_scheduling_menu()
            elif choice == '3':
                self.fee_tracking_menu()
            elif choice == '4':
                self.library_system_menu()
            elif choice == '5':
                self.performance_analytics_menu()
            elif choice == '6':
                self.run_demo_sequence()
            elif choice == '7':
                print("Thank you for using School Management System!")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    # Start up the school management system
    school_manager = SchoolManager()
    school_manager.run()