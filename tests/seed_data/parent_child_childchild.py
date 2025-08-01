import random

from sqlalchemy.orm import Session

from tests.model import SDChild, SDChildChild, SDParent


def generate_parent_child_object_hierarchy(
    s: Session, parent_id: int, min_children: int = 1, max_children: int = 5, parent_deleted: bool = False
):
    # Fix a seed in the RNG for deterministic outputs
    random.seed(parent_id)

    # Generate the Parent
    new_parent = SDParent(id=parent_id)
    new_parent.deleted_at = True if parent_deleted else False
    s.add(new_parent)
    s.flush()

    active_children = random.randint(min_children, max_children)
    deleted_children = random.randint(min_children, max_children)

    children = [False] * active_children + [True] * deleted_children

    # Create Children (SDChild)
    for child_no, child_deleted in enumerate(children):
        new_child_id = parent_id * 100 + child_no
        new_child = SDChild(id=new_child_id, parent_id=new_parent.id)
        new_child.deleted_at = True if child_deleted else False
        s.add(new_child)
        s.flush()

        # Create Child's Children (SDChildChild)
        active_child_children = random.randint(min_children, max_children)
        deleted_child_children = random.randint(min_children, max_children)

        child_children = [False] * active_child_children + [True] * deleted_child_children

        for child_children_no, child_children_deleted in enumerate(child_children):
            sdchild_child_id = new_child_id * 100 + child_children_no
            new_child_child = SDChildChild(id=sdchild_child_id, child_id=new_child.id)
            child_child_deleted = True if child_children_deleted else False
            new_child_child.deleted_at = child_child_deleted
            s.add(new_child_child)
            s.flush()

    s.commit()
