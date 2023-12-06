# Efficient Circular Deque Implementation with Application in Data Management

## Description

This project entails a comprehensive implementation of a Circular Double-Ended Queue (Deque), an advanced data structure that allows insertion and deletion at both ends. The project focuses on the efficient management of data, particularly in scenarios where memory optimization is critical, such as in network routers or undo operations in software applications.

## Project Files
- CDLL_DataManagement.py : contains full implementation. 

## Background

The Circular Deque is a versatile data structure that combines the characteristics of a standard queue and a stack. It is especially useful in applications where both FIFO (First-In-First-Out) and LIFO (Last-In-First-Out) operations are required. This implementation of the Circular Deque is unique in its circular nature, ensuring that memory usage is optimized by overwriting old elements as new ones are added.

## Implementation Details

Circular Array and Circular Doubly Linked List (CDLL): Two approaches to implement the Circular Deque, showcasing versatility in adapting to different application needs.

enqueue and dequeue Functions: Core operations for adding and removing elements from both ends of the deque. These functions are optimized for constant time complexity in most cases.

grow and shrink Functions: These functions dynamically adjust the size of the underlying structure, ensuring efficient use of memory. grow doubles the capacity of the deque, while shrink halves it, maintaining a minimum capacity.

Efficient Data Indexing: The implementation uses front and back pointers to ensure efficient access to the deque's ends, crucial for quick operations.
Application Problem: The Great List Rebellion

This imaginative scenario portrays a world where Python lists are patented, leading to the rise of the Circular Deque as an alternative data structure.

The project explores the use of the CDLL in a Circular Deque, termed CDLLCD, for efficient data handling, challenging the mainstream use of Python lists.
The application problem serves as a practical exercise in understanding the trade-offs between different data structure implementations, particularly in contexts where licensing and efficiency are crucial considerations.

## Key Features

Versatility in Data Handling: Capable of functioning as both a queue and a stack, adaptable for various practical applications.

Memory Optimization: Circular nature allows for efficient memory use, particularly beneficial in systems with limited memory resources.

Complexity Management: Amortized constant time complexity for enqueue and dequeue operations, ensuring performance efficiency.

## Technologies Used

Python

Data Structures (Circular Deque, Circular Array, CDLL)

## Setup and Installation

Clone the repository to your local machine.

Ensure Python is installed on your system.

Navigate to the project directory.

Run the main script to test the Circular Deque functionality.

## Usage

The Circular Deque can be used in applications where both queue-like and stack-like operations are needed.
It is particularly useful in scenarios like undo operations in software or packet management in network routers.
Contributions

Developed by: Shams Alkhalidy

Inspired by real-world scenarios and the need for efficient data structures in software development.

## Contact

For inquiries, please contact alkhali7@msu.edu.
