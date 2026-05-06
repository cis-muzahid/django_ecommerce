from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import Blog, BlogCategory
from home.management.commands._seed_image_utils import save_seed_image
from users.models import CustomUser


SEED_BLOG_CATEGORIES = [
    "Technology",
    "Lifestyle",
    "Health & Wellness",
    "Fashion & Style",
    "Home & Living",
    "Travel",
]

# image_dest is the leaf filename passed to FieldFile.save().
# Django prepends Blog.image upload_to='blog/images/' automatically,
# so the final stored path becomes  blog/images/<image_dest>.
SEED_BLOGS = [
    {
        "title": "Top 10 Smartphones of 2025",
        "description": (
            "We review the best smartphones released in 2025, covering performance, "
            "camera quality, battery life, and value for money. Whether you are an "
            "Android fan or an Apple loyalist, there is something for everyone."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "top-10-smartphones-2025",
        "category_name": "Technology",
        "active": True,
    },
    {
        "title": "How to Build a Productive Morning Routine",
        "description": (
            "Starting your day right can transform your productivity and mental health. "
            "In this post we share science-backed habits that successful people swear by, "
            "from mindful breathing to intentional goal-setting."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "productive-morning-routine",
        "category_name": "Lifestyle",
        "active": True,
    },
    {
        "title": "5 Superfoods You Should Add to Your Diet",
        "description": (
            "Nutrition experts reveal the top five superfoods that can boost immunity, "
            "improve digestion, and increase energy levels. Easy to find and even easier "
            "to incorporate into everyday meals."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "5-superfoods-for-your-diet",
        "category_name": "Health & Wellness",
        "active": True,
    },
    {
        "title": "Summer Fashion Trends to Watch",
        "description": (
            "From bold prints to minimalist silhouettes, this season's fashion scene is "
            "full of exciting directions. Our style editors break down the key trends "
            "and how to wear them without breaking the bank."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "summer-fashion-trends",
        "category_name": "Fashion & Style",
        "active": True,
    },
    {
        "title": "Budget Home Makeover Ideas That Actually Work",
        "description": (
            "You do not need a huge budget to refresh your living space. Discover "
            "creative DIY ideas, smart furniture choices, and colour palette tips "
            "that can completely transform any room."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "budget-home-makeover-ideas",
        "category_name": "Home & Living",
        "active": True,
    },
    {
        "title": "Hidden Gems: Underrated Travel Destinations for 2025",
        "description": (
            "Skip the tourist traps and explore these breathtaking destinations that "
            "most travellers overlook. From quiet coastal villages to vibrant mountain "
            "towns, adventure awaits off the beaten path."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "hidden-gem-travel-destinations-2025",
        "category_name": "Travel",
        "active": True,
    },
    {
        "title": "The Future of E-Commerce: Trends Shaping Online Shopping",
        "description": (
            "AI-powered recommendations, same-day delivery, and social commerce are "
            "redefining how we shop online. We explore the innovations that will "
            "dominate e-commerce over the next five years."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "future-of-ecommerce-trends",
        "category_name": "Technology",
        "active": True,
    },
    {
        "title": "Mindful Living: Simple Practices for a Calmer Life",
        "description": (
            "Mindfulness does not have to be complicated. This guide introduces "
            "practical, everyday techniques to reduce stress, improve focus, and "
            "cultivate a deeper sense of wellbeing."
        ),
        "image_file": "blog.jpeg",
        "image_dest": "blog.jpeg",
        "slug": "mindful-living-practices",
        "category_name": "Health & Wellness",
        "active": True,
    },
]

SEED_SUBDIR = "blogs"


class Command(BaseCommand):
    help = "Seed default blog categories and blog posts."

    def handle(self, *args, **options):
        admin_user = self._get_admin_user()
        if admin_user is None:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Run 'create_default_users' first."
                )
            )
            return

        # ── Blog categories (no images) ───────────────────────────────────
        category_map = {}
        cat_created  = 0
        cat_existing = 0

        with transaction.atomic():
            for cat_name in SEED_BLOG_CATEGORIES:
                cat, created = BlogCategory.objects.get_or_create(
                    name=cat_name,
                    defaults={"user": admin_user, "active": True},
                )
                category_map[cat_name] = cat
                if created:
                    cat_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  [+] Created blog category: {cat_name}")
                    )
                else:
                    cat_existing += 1
                    self.stdout.write(f"  [=] Blog category already exists: {cat_name}")

        # ── Blog posts ────────────────────────────────────────────────────
        blog_created   = 0
        blog_updated   = 0
        image_warnings = 0

        for data in SEED_BLOGS:
            category = category_map.get(data["category_name"])
            existing = Blog.objects.filter(slug=data["slug"]).first()

            if existing:
                # ── UPDATE ────────────────────────────────────────────────
                with transaction.atomic():
                    existing.description = data["description"]
                    existing.category    = category
                    existing.active      = data["active"]
                    existing.save(update_fields=["description", "category", "active"])

                if not (existing.image and existing.image.name):
                    ok = save_seed_image(
                        instance=existing,
                        field_name="image",
                        seed_subdir=SEED_SUBDIR,
                        filename=data["image_file"],
                        storage_upload_to=data["image_dest"],
                        stdout=self.stdout,
                        style=self.style,
                    )
                    if not ok:
                        image_warnings += 1

                blog_updated += 1
                self.stdout.write(f"  [=] Updated blog post: {existing.title}")

            else:
                # ── CREATE ────────────────────────────────────────────────
                # Step 1: insert the row with an empty image placeholder.
                with transaction.atomic():
                    blog = Blog.objects.create(
                        title=data["title"],
                        description=data["description"],
                        image="",  # placeholder — filled in step 2
                        slug=data["slug"],
                        user=admin_user,
                        category=category,
                        active=data["active"],
                    )

                # Step 2: upload through Django's storage backend.
                ok = save_seed_image(
                    instance=blog,
                    field_name="image",
                    seed_subdir=SEED_SUBDIR,
                    filename=data["image_file"],
                    storage_upload_to=data["image_dest"],
                    stdout=self.stdout,
                    style=self.style,
                )
                if not ok:
                    image_warnings += 1

                blog_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  [+] Created blog post: {data['title']}")
                )

        # ── Summary ───────────────────────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Blog categories: {cat_created} created, {cat_existing} already existed."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Blog posts: {blog_created} created, {blog_updated} updated."
            )
        )
        if image_warnings:
            self.stdout.write(
                self.style.WARNING(
                    f"  {image_warnings} blog post(s) had missing seed images. "
                    "Add the files to seed_assets/blogs/ and re-run."
                )
            )

    def _get_admin_user(self):
        user = CustomUser.objects.filter(is_superuser=True).first()
        if user is None:
            user = CustomUser.objects.filter(is_staff=True).first()
        return user
