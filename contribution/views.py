from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Contribution
from member.models import Member
from group.models import Group

# Function-based views
@login_required
def contribution_list(request):
    """Display all contributions"""
    contributions = Contribution.objects.all().order_by('-date', 'member__name')
    context = {
        'contributions': contributions,
        'title': 'All Contributions'
    }
    return render(request, 'contribution/contribution_list.html', context)

@login_required
def contribution_detail(request, pk):
    """Display contribution details"""
    contribution = get_object_or_404(Contribution, pk=pk)
    context = {
        'contribution': contribution,
        'title': f'Contribution: {contribution.member.name} - {contribution.date}'
    }
    return render(request, 'contribution/contribution_detail.html', context)

@login_required
def contribution_create(request):
    """Create a new contribution"""
    if request.method == 'POST':
        # Handle form submission
        member_id = request.POST.get('member')
        amount = request.POST.get('amount')
        contribution_type = request.POST.get('contribution_type', 'savings')
        date = request.POST.get('date')
        notes = request.POST.get('notes', '')
        
        if member_id and amount and date:
            try:
                member = Member.objects.get(id=member_id)
                contribution = Contribution.objects.create(
                    member=member,
                    amount=amount,
                    contribution_type=contribution_type,
                    date=date,
                    notes=notes
                )
                messages.success(request, f'Contribution of {amount} created successfully for {member.name}!')
                return redirect('contribution_detail', pk=contribution.pk)
            except Member.DoesNotExist:
                messages.error(request, 'Selected member does not exist.')
            except Exception as e:
                messages.error(request, f'Error creating contribution: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    members = Member.objects.all().order_by('name')
    context = {
        'members': members,
        'title': 'Add New Contribution'
    }
    return render(request, 'contribution/contribution_form.html', context)

@login_required
def contribution_update(request, pk):
    """Update contribution information"""
    contribution = get_object_or_404(Contribution, pk=pk)
    
    if request.method == 'POST':
        # Handle form submission
        member_id = request.POST.get('member')
        amount = request.POST.get('amount')
        contribution_type = request.POST.get('contribution_type')
        date = request.POST.get('date')
        notes = request.POST.get('notes', '')
        
        if member_id and amount and date:
            try:
                member = Member.objects.get(id=member_id)
                contribution.member = member
                contribution.amount = amount
                contribution.contribution_type = contribution_type
                contribution.date = date
                contribution.notes = notes
                contribution.save()
                messages.success(request, f'Contribution updated successfully!')
                return redirect('contribution_detail', pk=contribution.pk)
            except Member.DoesNotExist:
                messages.error(request, 'Selected member does not exist.')
            except Exception as e:
                messages.error(request, f'Error updating contribution: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    members = Member.objects.all().order_by('name')
    context = {
        'contribution': contribution,
        'members': members,
        'title': f'Edit Contribution: {contribution.member.name} - {contribution.date}'
    }
    return render(request, 'contribution/contribution_form.html', context)

@login_required
def contribution_delete(request, pk):
    """Delete a contribution"""
    contribution = get_object_or_404(Contribution, pk=pk)
    
    if request.method == 'POST':
        member_name = contribution.member.name
        amount = contribution.amount
        contribution.delete()
        messages.success(request, f'Contribution of {amount} for {member_name} deleted successfully!')
        return redirect('contribution_list')
    
    context = {
        'contribution': contribution,
        'title': f'Delete Contribution: {contribution.member.name} - {contribution.date}'
    }
    return render(request, 'contribution/contribution_confirm_delete.html', context)

@login_required
def member_contributions(request, member_id):
    """Display all contributions for a specific member"""
    member = get_object_or_404(Member, id=member_id)
    contributions = member.contributions.all().order_by('-date')
    
    total_savings = sum(c.amount for c in contributions if c.contribution_type == 'savings')
    total_loans = sum(c.amount for c in contributions if c.contribution_type == 'loan')
    
    context = {
        'member': member,
        'contributions': contributions,
        'total_savings': total_savings,
        'total_loans': total_loans,
        'title': f'Contributions for {member.name}'
    }
    return render(request, 'contribution/member_contributions.html', context)

@login_required
def group_contributions(request, group_id):
    """Display all contributions for a specific group"""
    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()
    
    # Get all contributions for group members
    contributions = Contribution.objects.filter(member__group=group).order_by('-date', 'member__name')
    
    total_savings = sum(c.amount for c in contributions if c.contribution_type == 'savings')
    total_loans = sum(c.amount for c in contributions if c.contribution_type == 'loan')
    
    context = {
        'group': group,
        'contributions': contributions,
        'total_savings': total_savings,
        'total_loans': total_loans,
        'title': f'Contributions for Group: {group.name}'
    }
    return render(request, 'contribution/group_contributions.html', context)

# Class-based views
class ContributionListView(ListView):
    model = Contribution
    template_name = 'contribution/contribution_list.html'
    context_object_name = 'contributions'
    ordering = ['-date', 'member__name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Contributions'
        return context

class ContributionDetailView(DetailView):
    model = Contribution
    template_name = 'contribution/contribution_detail.html'
    context_object_name = 'contribution'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Contribution: {self.object.member.name} - {self.object.date}'
        return context

class ContributionCreateView(CreateView):
    model = Contribution
    template_name = 'contribution/contribution_form.html'
    fields = ['member', 'amount', 'contribution_type', 'date', 'notes']
    success_url = reverse_lazy('contribution_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Contribution'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Contribution of {form.instance.amount} created successfully for {form.instance.member.name}!')
        return super().form_valid(form)

class ContributionUpdateView(UpdateView):
    model = Contribution
    template_name = 'contribution/contribution_form.html'
    fields = ['member', 'amount', 'contribution_type', 'date', 'notes']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Contribution: {self.object.member.name} - {self.object.date}'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Contribution updated successfully!')
        return super().form_valid(form)

class ContributionDeleteView(DeleteView):
    model = Contribution
    template_name = 'contribution/contribution_confirm_delete.html'
    success_url = reverse_lazy('contribution_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Contribution: {self.object.member.name} - {self.object.date}'
        return context
    
    def delete(self, request, *args, **kwargs):
        member_name = self.object.member.name
        amount = self.object.amount
        messages.success(request, f'Contribution of {amount} for {member_name} deleted successfully!')
        return super().delete(request, *args, **kwargs)
