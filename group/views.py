from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Group


@login_required
def group_list(request):
    groups = Group.objects.all().order_by('name')
    context = {
        'groups': groups,
        'title': 'All Groups'
    }
    return render(request, 'group/group_list.html', context)

@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    members = group.members.all().order_by('name')
    context = {
        'group': group,
        'members': members,
        'title': f'Group: {group.name}'
    }
    return render(request, 'group/group_detail.html', context)

@login_required
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cycle_start_date = request.POST.get('cycle_start_date')
        
        if name and cycle_start_date:
            try:
                group = Group.objects.create(
                    name=name,
                    cycle_start_date=cycle_start_date
                )
                messages.success(request, f'Group {group.name} created successfully!')
                return redirect('group_detail', pk=group.pk)
            except Exception as e:
                messages.error(request, f'Error creating group: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'title': 'Add New Group'
    }
    return render(request, 'group/group_form.html', context)

@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        cycle_start_date = request.POST.get('cycle_start_date')
        
        if name and cycle_start_date:
            try:
                group.name = name
                group.cycle_start_date = cycle_start_date
                group.save()
                messages.success(request, f'Group {group.name} updated successfully!')
                return redirect('group_detail', pk=group.pk)
            except Exception as e:
                messages.error(request, f'Error updating group: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'group': group,
        'title': f'Edit Group: {group.name}'
    }
    return render(request, 'group/group_form.html', context)

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, f'Group {group_name} deleted successfully!')
        return redirect('group_list')
    
    context = {
        'group': group,
        'title': f'Delete Group: {group.name}'
    }
    return render(request, 'group/group_confirm_delete.html', context)


class GroupListView(ListView):
    model = Group
    template_name = 'group/group_list.html'
    context_object_name = 'groups'
    ordering = ['name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Groups'
        return context

class GroupDetailView(DetailView):
    model = Group
    template_name = 'group/group_detail.html'
    context_object_name = 'group'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all().order_by('name')
        context['title'] = f'Group: {self.object.name}'
        return context

class GroupCreateView(CreateView):
    model = Group
    template_name = 'group/group_form.html'
    fields = ['name', 'cycle_start_date']
    success_url = reverse_lazy('group_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Group'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Group {form.instance.name} created successfully!')
        return super().form_valid(form)

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'group/group_form.html'
    fields = ['name', 'cycle_start_date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Group: {self.object.name}'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Group {form.instance.name} updated successfully!')
        return super().form_valid(form)

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'group/group_confirm_delete.html'
    success_url = reverse_lazy('group_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Group: {self.object.name}'
        return context
    
    def delete(self, request, *args, **kwargs):
        group_name = self.object.name
        messages.success(request, f'Group {group_name} deleted successfully!')
        return super().delete(request, *args, **kwargs)
