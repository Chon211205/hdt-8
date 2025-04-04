package src.main.java.com.estructuradatos.parte1;

import java.io.*;
import java.util.*;

class vecheap<E extends Comparable<E>> {
    private List<E> heap;

    public vecheap() {
        heap = new ArrayList<>();
    }

    public void insert(E item) {
        heap.add(item);
        Collections.sort(heap);
    }

    public E remove() {
        return heap.isEmpty() ? null : heap.remove(0);
    }
}
