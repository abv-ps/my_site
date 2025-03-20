from django.utils.translation import gettext_lazy as _, ngettext
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from django.views import View


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the main page.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The response containing the rendered main page template.
    """
    return render(
        request,
        'main/home.html', {
            'current_year': datetime.now().year,
            "services": ServiceView.SERVICES,
        }
    )


def about_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the 'About Us' page with company information.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The response containing the rendered 'About Us' page template.
    """
    about_title = _('About us')
    company_description = _('PrJSC "BOHUSLAVSKA SILHOSPTEKNIKA" is the largest in Ukraine '
                            'manufacturer of sprayers for agriculture and equipment '
                            'for application of liquid fertilizer.')

    product_line_title = _("The range of our products for plant protection includes:")

    trailed_sprayers_series = _(
        "trailed sprayers ODYSSEY, KRONOS, TITAN and ATLANT "
        "of 18m, 22m, 24m, 28m, 32m and 36m working width "
        "with capacity of 2000, 2500, 3000, 4000 liters plastic tanks")

    liquid_fertilizer_title = _("The range of our products for application of liquid fertilizer includes:")

    injection_applicators = _(
        "injection applicators LFM -3000-8.4 and LFM -5000-12;")

    fertilizer_applicators = _(
        "trailed plant-feeder for fertilizing PP-5000-01, "
        "PP-5000-02 and PP- 10 000-01")

    complete_set_for_applicator = _(
        "complete set of equipment for fertilizer applicator "
        "EKO-600-5.6 (for KRN-5.6m)")

    additional_services = _("We also perform the work on the re-equipment of cultivators "
                            "for injection of UAN (Nitrogen solutions) and of ammonia water.")

    expertise_description = _("Experienced staff, advanced technology, many years of experience "
                              "and attention we give to feedback from our customers ensures reliability "
                              "of our products. More than 5,000 trailed sprayers are operated "
                              "for plant protection in Ukraine, Kazakhstan, Moldova, Russia, Romania, "
                              "Lithuania, Bulgaria, Poland and Hungary.")

    slogan = _("Our machinery will protect your crop!")

    return render(
        request,
        'main/about.html', {
            'current_year': datetime.now().year,
            'about_title': about_title,
            'company_description': company_description,
            'product_line_title': product_line_title,
            'trailed_sprayers_series': trailed_sprayers_series,
            'liquid_fertilizer_title': liquid_fertilizer_title,
            'injection_applicators': injection_applicators,
            'fertilizer_applicators': fertilizer_applicators,
            'complete_set_for_applicator': complete_set_for_applicator,
            'additional_services': additional_services,
            'expertise_description': expertise_description,
            'slogan': slogan
        }
    )


class ContactView(View):
    """
    Renders the 'Contact Us' page containing contact information.

    This view is responsible for displaying the contact details, including the address,
    email, phone number, social media links, and working hours.
    """

    contact_title = _("Contact Information")
    address = _("Contact address: Ukraine, Kyiv, Pryrodna Street, 1")
    email = _("Email: abv@boguslav.ua")
    phone = _("Phone: +380 (44) 123-45-67")
    social_media = _("We are also on social media!")
    working_hours = _("Working hours: Mon-Fri 08:00 - 16:30")

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Renders the 'Contact Us' page.

        Parameters:
            request (HttpRequest): The request object from the user.

        Returns:
            HttpResponse: The response containing the rendered 'Contact Us' page template.
        """
        return render(request,
                      'main/contact.html', {
                          'current_year': datetime.now().year,
                          'contact_title': self.contact_title,
                          'address': self.address,
                          'email': self.email,
                          'phone': self.phone,
                          'social_media': self.social_media,
                          'working_hours': self.working_hours
                      }
                      )


class ServiceView(View):
    """
    Renders the 'Our Services' page containing a list of services provided by the company.

    This view handles the display of various services offered, with options for searching
    and filtering the services based on user input.
    """

    services_title = _("Our Services")
    last_updated = datetime.now()
    last_updated_view = _("Last updated:")
    search_view = _("Search")
    total_services_view = _("Total")
    contacts_availability_view = _("Contacts available:")
    no_services_view = _("No services available")
    yes_no_view = _("Yes,No")
    show_all = _("Show all services")
    show_not_all = _("Collapse")
    show_all_text = _("Show all text")

    SERVICES = [
        {
            "title": _("Seed Drills Retrofit for Fertilizer Application"),
            "description": _(
                "We provide retrofitting services for seed drills to enable the application "
                "of nitrogen fertilizers (CAS) directly during planting. Our solutions increase "
                "the efficiency and productivity of agricultural equipment."
            ),
        },
        {
            "title": _("Custom Machinery Modifications"),
            "description": _(
                "We offer customized machinery modifications to optimize the performance "
                "of your equipment, adapting it to the specific needs "
                "of your agricultural operations."
            ),
        },
        {
            "title": _("Installation of Fertilizer Equipment"),
            "description": _(
                "We install state-of-the-art fertilizer application systems, ensuring accurate "
                "and efficient application of liquid and granular fertilizers to improve crop yield."
            ),
        },
        {
            "title": _("Machine Overhaul and Repair"),
            "description": _(
                "We specialize in the overhaul and repair of seed drills "
                "and other agricultural machinery, restoring them to peak performance."
            ),
        },
        {
            "title": _("Consulting on Agricultural Machinery"),
            "description": _(
                "We offer expert consulting on selecting, operating, "
                "and maintaining agricultural machinery for optimal performance and cost-efficiency."
            ),
        },
    ]

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Renders the 'Our Services' page with filtered services based on user input.

        Parameters:
            request (HttpRequest): The request object from the user.

        Returns:
            HttpResponse: The response containing the rendered 'Our Services' page template.
        """
        query = request.GET.get("q", "").strip().lower()
        filtered_services = [
            s for s in self.SERVICES if query in s["title"].lower()
        ] if query else self.SERVICES

        show_all = request.GET.get('show_all') == 'true'
        services_all_count = len(self.SERVICES)
        services_to_display = filtered_services if show_all else filtered_services[:3]
        service_view = ngettext("service", "services", len(services_to_display))

        context = {
            "current_year": datetime.now().year,
            "services_title": self.services_title,
            "services": services_to_display,
            "filtered_services": filtered_services,
            "last_updated": self.last_updated,
            "search_placeholder": _("Search services..."),
            "has_contacts": True,
            "last_updated_view": self.last_updated_view,
            "search_view": self.search_view,
            "total_services_view": self.total_services_view,
            "services_all_count": services_all_count,
            "service_view": service_view,
            "contacts_availability_view": self.contacts_availability_view,
            "no_services_view": self.no_services_view,
            "yes_no_view": self.yes_no_view,
            "show_all": self.show_all,
            "show_not_all": self.show_not_all,
            "show_all_text": self.show_all_text,
        }

        return render(request, "main/services.html", context)


def services_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the list of services, with options to show all or a limited set.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The response containing the rendered services page.
    """
    show_all = request.GET.get('show_all') == 'true'
    if show_all:
        services = ServiceView.SERVICES
    else:
        services = ServiceView.SERVICES[:3]
    return render(request, 'main/services.html', {'services': services})
